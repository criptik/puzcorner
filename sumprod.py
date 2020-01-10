import sys
import math
from functools import reduce
from abc import ABC, abstractmethod

shown1 = False

def lowfactors(n):    
    return set(reduce(list.__add__, 
                ([i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

class SearchBase(ABC):
    def initSearch(self, num):
        self.tries = 0
        self.solutions = []
        self.goal = num * 1000000
        
    def addSolution(self, n1, n2, n3, n4):
        self.solutions.append([n1/100, n2/100, n3/100, n4/100])
        # print(self.solutions)
        
    def getTries(self):
        return self.tries

    @abstractmethod
    def search(self, num):
        pass
    
class SumFirst(SearchBase):
    def search(self, num):
        self.initSearch(num)
        n1top = int(self.goal**0.25) + 1
        for n1 in range(1, n1top):
            # print('.', end='')
            if self.goal % n1 != 0:
                continue
            if shown1:
                print(n1)
            n2top = int((self.goal/n1)**0.333) + 1
            for n2 in range(n1, n2top):
                if self.goal % (n1 * n2) != 0:
                    continue
                n3n4sum = num - (n1 + n2)
                n3n4prod = self.goal // (n1 * n2)
                rootprod = math.sqrt(n3n4prod)
                for n3 in range(n2, int(rootprod) + 1):
                    if n3 > int(n3n4sum/2) + 1:
                        break
                    self.tries = self.tries + 1
                    if n3n4prod % n3 != 0:
                        continue
                    n4 = n3n4prod // n3
                    if n3 + n4 == n3n4sum:
                        self.addSolution(n1, n2, n3, n4)
                        break
                    
        # finished search, return solutions if any
        return self.solutions        


class ProdFirst(SearchBase):
    def search(self, num):
        self.initSearch(num)
        n1top = int(self.goal/4) + 1
        # print(num, n1top)
        for n1 in range(1, n1top):
            if self.goal % n1 != 0:
                continue
            if n1 >= num/4 + 1:
                break
            if shown1:
                print(n1)
            n2goal = self.goal // n1
            n2top = int(n2goal/3) + 1
            for n2 in range(n1, n2top):
                if n2goal % n2 != 0:
                    continue
                if n1+n2 >= num:
                    break
                n3goal = n2goal // n2
                n3n4sum = num - (n1 + n2)
                n3top = int(n3goal/2) + 1
                for n3 in range(n2, n3top):
                    if n3 > int(n3n4sum/2) + 1:
                        break
                    self.tries = self.tries + 1
                    if n3goal % n3 != 0:
                        continue
                    n4 = n3goal // n3
                    if n1+n2+n3 >= num:
                        break
                    if n3 + n4 == n3n4sum:
                        self.addSolution(n1, n2, n3, n4)
                        break

        # finished search, return solutions if any
        return self.solutions        

# searcher = SumFirst()
numlo = int(sys.argv[1]) if len(sys.argv) >= 2 else 710
numhi = int(sys.argv[2]) if len(sys.argv) >= 3 else 712
searcher = SumFirst() if len(sys.argv) >= 4 else ProdFirst() 
print('%s search' % (searcher.__class__.__name__))

totalFinds = 0
nonzNums = 0
maxFinds = 0
totTries = 0
for num in range (numlo, numhi):
    sols = searcher.search(num)
    tries = searcher.getTries()
    totTries = totTries + tries
    finds = 0
    for sol in sols:
        print ('... %.2f: %.2f %.2f %.2f %.2f' % (num/100, sol[0], sol[1], sol[2], sol[3]))
        finds = finds + 1

    if finds > 0:
        print('          %d find%s after %d tries' % (finds, 's' if finds > 1 else '', tries) )
        totalFinds = totalFinds + finds
        nonzNums = nonzNums + 1
        if finds > maxFinds:
            maxFinds = finds
            maxFindsList = [num/100]
        elif finds == maxFinds:
            maxFindsList.append(num/100)
            
print('TotalTries = %d on %d numbers' % (totTries, numhi-numlo))
print('%d total finds on %d numbers' % (totalFinds, nonzNums))
print('Max Finds = %d on ' % (maxFinds),
      '[', ''.join('%.2f, ' % (k) for k in maxFindsList), ']')




            
