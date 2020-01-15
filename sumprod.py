import sys
import math
from functools import reduce
from abc import ABC, abstractmethod
import argparse

shown1 = False
debug = False
global args

def lowfactors(n):    
    return set(reduce(list.__add__, 
                ([i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

def parse_args():
    parser = argparse.ArgumentParser(description='Puzzle Corner 4-item Sum = Prod')

    parser.add_argument('--range', type=int, nargs='+', default=[711], help='range of values to test')
    parser.add_argument('--count', type=int, default=4, help='number of items in search')
    parser.add_argument('--prod-first', default=False, action='store_true', help='true to use ProdFirst search') 
    parser.add_argument('--debug', default=False, action='store_true', help='print some debug info') 
    return parser.parse_args()

class SearchBase(ABC):
    def initSearch(self, num, itemCount):
        self.tries = 0
        self.solutions = []
        self.num = num
        self.goal = num * 100**(itemCount - 1)
        self.itemCount = itemCount
        self.vals = [None] * (itemCount+1)
        
    def addSolution(self):
        if args.debug:
            print('adding solution %s' % self.vals)
        solvals = []
        for val in self.vals:
            if val is not None:
                solvals.append(val/100)
        self.solutions.append(solvals)
        
    def getTries(self):
        return self.tries

    def n1TooSmall(self, n1):
        # if n1 is too small to reach goal, skip
        # would be nice if there was an easy way to compute this "n1bot"
        # print(num, n1)
        left = (self.goal/n1) ** (1/(self.itemCount - 1))
        right = (self.num-n1)/(self.itemCount - 1)
        return left > right

    def n1FindTop(self):
        n1topa = int(self.goal**(1/self.itemCount)) + 1
        n1topb = int(self.goal/self.itemCount) + 1
        return min(n1topa, n1topb)

    def findLastTwo(self, prev, last2sum, last2prod):
        if True:
            # this solves directly for the last two vals
            self.tries = self.tries + 1
            rootterm = last2sum**2 - 4*last2prod
            # if rootterm not valid, choose a different n2
            if rootterm < 0:
                return None
            sol = (last2sum - math.sqrt(rootterm)) / 2
            if sol != int(sol):
                return None
            # must not be less than previous value
            if sol >= prev:
                return sol
        else:
            # old slower search way kept around for no good reason
            rootprod = math.sqrt(last2prod)
            for n3 in range(prev, int(rootprod) + 1):
                if n3 > int(last2sum/2) + 1:
                    return None
                self.tries = self.tries + 1
                if last2prod % n3 != 0:
                    continue
                n4 = last2prod // n3
                if n3 + n4 == last2sum:
                    return n3

        
    @abstractmethod
    def search(self, num, itemCount):
        pass
    
class SumFirst(SearchBase):
    def nextItemCost(self, itemIndex, start, end, sum, prod):
        # if only two left, find them and return
        if (itemIndex == self.itemCount - 1):
            penult = self.findLastTwo(start, sum, prod)
            if penult is not None:
                ult = sum - penult
                self.vals[itemIndex] = penult
                self.vals[itemIndex+1] = ult
                self.addSolution()
        else:
            # else not a lastTwo case, check and recurse
            for val in range(start, end):
                # print('.', end='')
                if itemIndex == 1 and self.n1TooSmall(val):
                        continue
                if prod % val != 0:
                    continue
                if args.debug:
                    print('itemIndex=%d, sum=%d, prod=%d, val=%d, vals=%s' % (itemIndex, sum, prod, val, self.vals))
                self.vals[itemIndex] = val
                nexttop = int((prod // val)**(1/(self.itemCount - itemIndex))) + 1
                self.nextItemCost(itemIndex+1, val, nexttop, sum - val, prod//val)
                
            
    def search(self, num, itemCount):
        self.initSearch(num, itemCount)
        n1top = self.n1FindTop()
        self.nextItemCost(1, 1, n1top, self.num, self.goal)
                    
        # finished search, return solutions if any
        return self.solutions        


class ProdFirst(SearchBase):
    def search(self, num, itemCount):
        print('ProdFirst not currently supported')
        sys.exit()
        self.initSearch(num, itemCount)
        # print(num, n1top)
        
        n1top = self.n1FindTop()
        for n1 in range(1, n1top):
            if self.n1TooSmall(n1):
                continue
            if self.goal % n1 != 0:
                continue
            if n1 >= num/4 + 1:
                break
            if args.debug:
                print(n1, end=' ')
            n2goal = self.goal // n1
            n2top = int(n2goal/3) + 1
            for n2 in range(n1, n2top):
                if n2goal % n2 != 0:
                    continue
                if n1+n2 >= num:
                    break
                n3n4prod = n2goal // n2
                n3n4sum = num - (n1 + n2)
                n3 = self.findLastTwo(n2, n3n4sum, n3n4prod)
                if n3 is not None:
                    n4 = n3n4sum - n3
                    self.addSolution(n1, n2, n3, n4)
                            
        # finished search, return solutions if any
        return self.solutions        

args = parse_args()
if len(args.range) == 1:
    args.range.append(args.range[0] + 1)
searcher = ProdFirst() if (args.prod_first) else SumFirst()
print('%s search for %d items on range %s' % (searcher.__class__.__name__, args.count, args.range))

totalFinds = 0
nonzNums = 0
maxFinds = 0
totTries = 0
itemCount = args.count
for num in range (args.range[0], args.range[1]):
    sols = searcher.search(num, itemCount)
    tries = searcher.getTries()
    totTries = totTries + tries
    finds = 0
    for sol in sols:
        finds = finds + 1
        noPennies = True
        billsOnly = True
        for n in range(itemCount):
            cents = sol[n] * 100
            if cents % 10 != 0:
                noPennies = False
                billsOnly = False
                break
            elif cents % 100 != 0:
                billsOnly = False
                
        print ('... %.2f: %s   %s' %
               (num/100, ''.join('%.2f ' % (k) for k in sol), '!!!!!!' if billsOnly else '!!!' if  noPennies else ''))
        
    if finds > 0:
        print('          %d find%s after %d tries' % (finds, 's' if finds > 1 else '', tries) )
        totalFinds = totalFinds + finds
        nonzNums = nonzNums + 1
        if finds > maxFinds:
            maxFinds = finds
            maxFindsList = [num/100]
        elif finds == maxFinds:
            maxFindsList.append(num/100)
            
print('TotalTries = %d on %d numbers' % (totTries, args.range[1] - args.range[0]))
print('%d total finds on %d numbers' % (totalFinds, nonzNums))
if maxFinds > 0:
    print('Max Finds = %d on ' % (maxFinds),
          '[%s]' % ''.join('%.2f, ' % (k) for k in maxFindsList))




            
