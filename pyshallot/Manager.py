import multiprocessing
from queue import Empty as QueueEmpty
from os.path import isdir
from os import makedirs

from typing import List

from pyshallot.Worker import Worker


class Manager(object):
    results = multiprocessing.Queue()
    trials = multiprocessing.Queue()
    kill = multiprocessing.Event()
    processes = []

    do_run = False
    prev_found = 0
    found = []

    def __init__(self, threads: int, patterns: List[str], directory: str, one: bool):
        self.threads = threads
        self.patterns = patterns
        self.one = one
        if not directory.endswith("/"):
            directory += "/"
        self.directory = directory
        self.do_run = True

    def _create_directories(self):
        for pattern in self.patterns:
            d = self.directory + pattern + "/"
            if not isdir(self.directory):
                makedirs(d, exist_ok=True)

    def start(self):
        self._create_directories()

        for i in range(self.threads):
            self.processes.append(Worker(self.patterns, self.results, self.trials, self.kill))
            self.processes[i].start()

        self.run()

    def run(self):
        while self.do_run:
            try:
                self.found.append(self.results.get(True, 0.1))
                if self.one and len(self.found) == 1:
                    self.do_run = False
                    self.kill.set()
                    return self.found[0]
                l = len(self.found)
                if l > self.prev_found:
                    print("Found: ")
                    for i in range(l - self.prev_found):
                        print("\t", self.found[i][:22])
                self.prev_found = len(self.found)
            except QueueEmpty:
                pass
            else:
                break

    def stop(self):
        self.do_run = False
        """joins all processes, empties all queues, and returns sum of trials."""
        if not self.kill.is_set():
            self.kill.set()
        sum_trials = 0
        while not self.trials.empty():
            sum_trials += self.trials.get()
        for proc in self.processes:
            proc.join()
        while not self.results.empty():
            self.results.get()
        return sum_trials
