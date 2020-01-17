import sys
import math
from abc import ABC, abstractmethod
import argparse

# From this problem in 2020 J/F
#
# Richard Thornton sometimes overpays, since he occasionally
# multiplies the costs of individual items instead of summing
# them. (We assume all items cost a positive integral multiple of
# cents.) One time, he purchased four items whose total cost is $7.11,
# but he was lucky since the product was also $7.11. What did the
# individual items cost?


global args

def parse_args():
    parser = argparse.ArgumentParser(description='Puzzle Corner 4-item Sum = Prod')
    parser.add_argument('--totals', type=int, nargs='+', default=[711], help='range of values to test (in whole cents)')
    parser.add_argument('--items', type=int, nargs='+', default=[4], help='range of number of items in search')
    parser.add_argument('--debug', default=False, action='store_true', help='print some debug info') 
    return parser.parse_args()

class SearchBase(ABC):
    def initSearch(self, num, itemCount):
        self.tries = 0
        self.solutions = []
        self.num = num
        self.goal = num * 100**(itemCount - 1)
        self.itemCount = itemCount
        self.vals = [None] * (itemCount)
        
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
                self.vals[itemIndex-1] = penult
                self.vals[itemIndex] = ult
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
                self.vals[itemIndex-1] = val
                nexttop = int((prod // val)**(1/(self.itemCount - itemIndex))) + 1
                self.nextItemCost(itemIndex+1, val, nexttop, sum - val, prod//val)
                
            
    def search(self, num, itemCount):
        self.initSearch(num, itemCount)
        n1top = self.n1FindTop()
        self.nextItemCost(1, 1, n1top, self.num, self.goal)
                    
        # finished search, return solutions if any
        return self.solutions        



args = parse_args()
numlo = args.totals[0]
numhi = numlo + 1 if len(args.totals) == 1 else args.totals[1]+1
itemslo = args.items[0]
itemshi = itemslo + 1 if len(args.items) == 1 else args.items[1]+1
searcher = SumFirst()
print('%s search for %s items on range %s' % (searcher.__class__.__name__, args.items, args.totals))

totalFinds = 0
nonzNums = 0
maxFinds = 0
totTries = 0
for num in range (numlo, numhi):
    for itemCount in range (itemslo, itemshi):
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

            print ('(%d)... %.2f: %s   %s' %
                   (itemCount, num/100,
                    ''.join('%.2f ' % (k) for k in sol), '!!!!!!' if billsOnly else '!!!' if  noPennies else ''))
        
        if finds > 0:
            print('          %d find%s after %d tries' % (finds, 's' if finds > 1 else '', tries) )
            totalFinds = totalFinds + finds
            nonzNums = nonzNums + 1
            if finds > maxFinds:
                maxFinds = finds
                maxFindsList = [(num/100, itemCount)]
            elif finds == maxFinds:
                maxFindsList.append((num/100, itemCount))
            
print('TotalTries = %d on %d numbers' % (totTries, numhi - numlo))
print('%d total finds on %d number/count combos' % (totalFinds, nonzNums))
# print(maxFindsList)
if maxFinds > 0:
    print('Max Finds = %d on [%s]' %
          (maxFinds, ''.join('%.2f (%d), ' % (num, count) for (num, count) in maxFindsList)))




            
