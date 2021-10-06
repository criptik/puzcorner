# Formula is 2*N**2 = S(S+1)
# N = Alice's #
# S = total on street
# S**2 + S - 2*N**2 = 0
# so given S
# 2*N**2 = S**2 + S
# N = sqrt((S**2 + S) / 2)

# to speed things up we note that either S or S+1 must be an odd square
# using this logic
# (S * (S + 1)) / 2  has to be an integer squared
# We know one of N and N+1 is even and odd
# assume neither N nor N+1 is a square
# then one of them will have a factor x >= 3 which is not a factor of the other

# Now assume the even one is a square.  Then again the odd will have a
# factor x >= 3 which is not a factor of the other.

# Thus one of N and N+1 must be an odd square.

import math
import gmpy2
from abc import ABC, abstractmethod
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Puzzle Corner House Number Problem')
    parser.add_argument('--low', type=int, default=3, help='low number of Alice house # for search')
    parser.add_argument('--high', type=int, default=10000000, help='high number of Alice house # for search')
    parser.add_argument('--alg', default='faost', help='search algorithm to use')
    return parser.parse_args()


class SearchBase(ABC):
    def __init__(self, args):
        self.args = args

    def printFind(self, N, S, extraStr=''):
        print(f'house {N:,d} out of {S:,d} {extraStr}')

        
    @abstractmethod
    def search(self):
        pass

class SlowSearch(SearchBase):
    def search(self):
        for N in range (self.args.low, self.args.high):
            prod = 1 + 8 * N * N
            if not gmpy2.is_square(prod):
                continue
            root = math.isqrt(prod)
            S = root - 1 // 2
            self.printFind(N, S)


class FastSearch(SearchBase):
    def search(self):
        lolim = max(math.isqrt(self.args.low), 3)
        # ensure odd
        if lolim % 2 == 0:
            lolim = lolim + 1
        hilim = math.isqrt(2 * self.args.high)
        print(f'hilim = {hilim}')
        
        for oddnum in range (lolim, hilim, 2):
            oddsq = oddnum*oddnum
            for fix in [1, -1]:
                evensqdoub = oddsq + fix
                evensq = evensqdoub // 2
                if not gmpy2.is_square(evensq):
                    continue
                evennum = math.isqrt(evensq)
                root = oddnum * evennum
                N = root
                if N > self.args.high:
                    return
                S = min(oddsq,evensqdoub)
                self.printFind(N, S, f'    ({evennum} * {oddnum})')
                break
        print(f'oddnum = {oddnum}')
    
    
#------- main program ------------
args = parse_args()
searcher = FastSearch(args) if args.alg == 'fast' else SlowSearch(args)
searcher.search()
