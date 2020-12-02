import multiprocessing

from argparse import ArgumentParser

from pyshallot.RSA import pprint_privkey
from pyshallot.Manager import Manager


# Main thread
def main():
    ap = ArgumentParser()
    ap.add_argument("-p", "--pattern", type=str, help="pattern to search for", required=True)
    ap.add_argument("-t", "--threads", type=int, default=multiprocessing.cpu_count(), help="processes to start")
    ap.add_argument("-o", "--one", action="store_true", help="Stop after the first find.")
    ap.add_argument("-d", "--directory", type=str, default="searches/", help="Write results here.")
    a = ap.parse_args()

    m = Manager(a.threads, a.pattern, a.directory, a.one)

    try:
        m.start()
    except KeyboardInterrupt:
        m.stop()
        pass

    sum_trials = m.stop()
    print('Tried', sum_trials, 'public keys before exit')

    for f in m.found:
        onion = f[:22]
        privkey = f[22:]
        print('-' * 64)
        print('Found matching pattern after', sum_trials, 'tries:', onion)
        print('-' * 64)
        pprint_privkey(privkey)


if __name__ == '__main__':
    main()
