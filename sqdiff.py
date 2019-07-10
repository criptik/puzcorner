import sys
import math
import argparse

class DiffInfo(object):
    def __init__(self):
        self.ary = []
        self.len = 0
        self.umap = {}
        
    def addtup(self, tup):
        self.ary.append(tup)
        self.len += 1
        (m, n) = tup
        self.umap[m] = 1
        self.umap[n] = 1

    def all_unique(self):
        return len(self.umap.keys()) == self.len * 2
    
class DiffSet(object):
    def __init__(self, allowDups):
        self.map = {}
        self.maxcount = 0
        self.allowDups = allowDups
        self.maxes = []           

    def add_top_col(self, top):
        for m in range (1, top-1):
            diff = top*top - m*m
            if self.map.get(diff) == None:
                self.map[diff] = DiffInfo()
            self.map[diff].addtup((m, top))
            newlen = self.map[diff].len
            if newlen >= self.maxcount and (self.allowDups or self.map[diff].all_unique()):
                if newlen > self.maxcount:
                    self.maxcount = newlen
                    self.maxes = []
                self.maxes.append(diff)

    def find_maxes(self):
        # find the ones with the biggest count and optionally all unique
        return self.maxes

    # show the maxes
    def show_maxes(self, maxes):
        for diff in maxes:
            count = self.map[diff].len
            print('%d: (%d%s) %s' % (diff, count, (' U' if self.map[diff].all_unique() else ''), self.map[diff].ary))
            print(primeFactors(diff))
            print()
        
        
    
def parse_args():
    parser = argparse.ArgumentParser(description='Puzzle Corner diff of squares app')

    parser.add_argument('--low', type=int, default=2, help='low value for scan')
    parser.add_argument('--high', type=int, default=100, help='high value for scan or single value for single')
    parser.add_argument('--action', default='single', help='single=show for single value at high, scan=scan from low to high')
    parser.add_argument('--allow-dups', default=False, action='store_true', help='true if duplicates allowed between tuples')
    return parser.parse_args()

# A function to print all prime factors of  
# a given number n 
def primeFactors(n): 
    ans = []
    
    # Print the number of two's that divide n 
    while n % 2 == 0: 
        ans.append(2)
        n = n / 2
          
    # n must be odd at this point 
    # so a skip of 2 ( i = i + 2) can be used 
    for i in range(3,int(math.sqrt(n))+1,2): 
        # while i divides n , print i ad divide n 
        while n % i== 0: 
            ans.append(i)
            n = n / i 
              
    # Condition if n is a prime 
    # number greater than 2 
    if n > 2: 
        ans.append(int(n))
    return ans


def try_with_top(dset, top):
    for m in range(2, top+1):
        dset.add_top_col(m)

    return dset.find_maxes()
    

            
args = parse_args()
if args.action == 'single':
    dset = DiffSet(args.allow_dups)
    maxes = try_with_top(dset, args.high)
    dset.show_maxes(maxes)

else:
    maxmax = 0
    dset = DiffSet(args.allow_dups)
    # seed with args.low
    maxes = try_with_top(dset, args.low)
    for xtop in range(args.low+1, args.high):
        dset.add_top_col(xtop)
        
        if dset.maxcount > maxmax:
            maxmax = dset.maxcount
            print(xtop, dset.maxcount)
        
        
