from time import time

from platform import processor

from json import dump

from tqdm import tqdm

from pyshallot import Worker


ONE = ["a", "b", "c", "d", "e"]
TWO = ["aa", "is", "ja", "ok", "we"]
THREE = ["two", "yes", "bye", "she", "the"]
FOUR = ["flex", "like", "icke", "term", "aaaa"]
FIVE = ["david", "terms", "model", "robot", "prefix"]
SIX = ["robots", "aaaaaa", "noodle", "github", "gazebo"]
SEVEN = ["systems", "aaaaaaa", "command", "related", "section"]
EIGHT = ["binaries", "aaaaaaaa", "openrave", "planners", "internal"]
NINE = ["aaaaaaaaa", "important", "kinematic", "exception", "framework"]
TEN = ["aaaaaaaaaa", "developing", "automation", "simulation", "completion"]
ELEVEN = ["aaaaaaaaaaa", "environment", "application", "development", "acknowledge"]
TWELVE = ["aaaaaaaaaaaa", "instructions", "dependencies", "alternatives", "applications"]

LENGTHS = [ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, ELEVEN, TWELVE]
THREADS = 1

m = len(LENGTHS[0]) * len(LENGTHS)


'''
we are measuring time / word length
but we can plot this later, for now we just write it into a json structure
'''

RESULTS = []
i = 0
bar = tqdm(total=m)


def timeit(pattern: str) -> float:
    s = time()
    r = new_worker(pattern).find()[0][:22]
    bar.set_description("%s" % r)
    r = time() - s
    return r


def new_worker(pattern: str) -> Worker:
    return Worker([pattern], one=True)


for l in LENGTHS:
    lres = []
    print(l)
    for w in l:
        lres.append(timeit(w))
        i += 1
        bar.update(i)
    RESULTS.append(lres)

with open("results.json", "w") as o:
    dump({
        "processor": processor(),
        "results": RESULTS
    }, o)
