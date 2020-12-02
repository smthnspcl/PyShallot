import re
import os
import gmpy2
from functools import reduce
from multiprocessing import Queue, Event, Process

from typing import List

from pyshallot.RSA import private_key, make_onion

# Constants stolen from the original shallot ####
EMIN = 0x10001
EMAX = 0xFFFFFFFFFF


def good_prime(p):
    """True if highly probably prime, else false."""
    return gmpy2.is_prime(p, 1000) and gmpy2.is_strong_bpsw_prp(p)


# Prime finding stuff for RSA ####
def random(bytez):
    """Produces a random number thats has bytez*8 amount of bits."""
    return gmpy2.mpz(reduce(lambda a, b: (a << 8) | ord(chr(b)), os.urandom(bytez), 0))


def find_prime(bytez=128):
    """Checks random numbers for primality"""
    p = random(bytez) | 1
    while not good_prime(p):
        p = random(bytez) | 1
    return p


def good_pair(p, q):
    """Returns p*q if p and q are a good pair, else 0."""
    n = p * q
    k = gmpy2.ceil(gmpy2.log2(n))
    if abs(p - q) > 2 ** (k / 2 - 100):
        return n
    return 0


# Worker process generates keys, hashes, and checks for patterns
class Worker(Process):
    patterns: List[str] = []
    regexes: List[re.Pattern] = []
    results = None
    trials = None
    kill = None
    one = False

    def __init__(self, patterns: List[str], results=Queue(), trials=Queue(), kill=Event(), one=False, *args, **kwds):
        Process.__init__(self, *args, **kwds)
        self.patterns = patterns
        self.results = results
        self.trials = trials
        self.kill = kill
        self.one = one
        self._build_regexes()

    def _build_regexes(self):
        for pattern in self.patterns:
            self.regexes.append(re.compile(pattern))

    @staticmethod
    def find_good_pair():
        r = None
        while not r:
            p = find_prime()
            q = find_prime()
            if q > p:
                p, q = q, p
            n = good_pair(p, q)
            if n:
                return n, p, q

    def matches_regex(self, onion):
        for regex in self.regexes:
            if regex.search(onion):
                print(regex, onion)
                return True
        return False

    def find(self):
        i = 0
        while True:
            n, p, q = self.find_good_pair()
            t = n - (p + q - 1)
            e = EMIN
            while e < EMAX:
                if self.kill.is_set():
                    self.trials.put(i)
                    return
                i += 1
                o = make_onion(n, e)
                if self.matches_regex(o.decode('utf-8')) and gmpy2.gcd(e, t) == 1:
                    d = gmpy2.invert(e, t)
                    p = private_key(n, e, d, p, q)
                    if self.one:
                        self.kill.set()
                        return o, p
                    else:
                        self.results.put(o + p)
                        self.trials.put(i)
                e += 2

    def run(self):
        self.find()
