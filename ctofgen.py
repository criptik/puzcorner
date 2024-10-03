import collections
import sys
import argparse

# just some brute force searches for various patterns


def parse_args():
    parser = argparse.ArgumentParser(description='C to F brute force searcher')
    parser.add_argument('--low', type=int, default=1000, help='low val for search')
    parser.add_argument('--high', type=int, default=100000, help='high val for search')
    parser.add_argument('--stopOnFirst', default=False, action='store_true', help='whether to stop on first solution')
    parser.add_argument('--searcher', default='ShuffleDigits', help='searcher class to use')
    
    return parser.parse_args()

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)    


class ShuffleDigits:
    def isTrue(self, C, F):
        counterF = collections.Counter(list(str(F)))
        counterC = collections.Counter(list(str(C)))
        return counterF == counterC
    
    def step(self):
        return 5

    def modStartList(self):
        return [0,5]

class ReverseDigits:
    def isTrue(self, C, F):
        return F == self.reverseNumber(C)

    def reverseNumber(self, number):
        numList = list(str(number))
        reversedNum = int(''.join(numList[::-1]))
        return reversedNum
    
    def step(self):
        return 10

    def modStartList(self):
        return [5]
    
class RotateRight:
    def isTrue(self, C, F):
        # print(C, F, self.rotateRightNumber(C))
        return F == self.rotateRightNumber(C)

    def rotateRightNumber(self, number):
        numList = list(str(number))
        tmp = numList[-1]
        for n in range(len(numList)-1, 0, -1):
            numList[n] =  numList[n-1]
        numList[0] = tmp
        rotatedNum = int(''.join(numList))
        return rotatedNum
    
    def step(self):
        return 10

    def modStartList(self):
        return [5]
    
class SwapFirstLast:
    def isTrue(self, C, F):
        # print(C, F, self.rotateRightNumber(C))
        return F == self.swapFirstLastNumber(C)

    def swapFirstLastNumber(self, number):
        numList = list(str(number))
        tmp = numList[0]
        numList[0] = numList[-1]
        numList[-1] = tmp
        swappedNum = int(''.join(numList))
        return swappedNum
    
    def step(self):
        return 10

    def modStartList(self):
        return [5]
    

def endProgram():
    sys.exit(0)
    
# main code:
#for tst in [1234, 12345]:
#    print(tst, swapFirstLastNumber(tst))
#    print(tst, reverseNumber(tst))

args = parse_args()
searcher = str_to_class(args.searcher)()
C = args.low
# advance until C meets the modstart requirement
while C % 10 not in searcher.modStartList():
    C += 1
# print(C)

while C < args.high:
    #if C % 10000000 in searcher.modStartList():
    #    print(f'{C}...')
    F = 9 * C // 5 + 32
    if searcher.isTrue(C, F):
        print(args.searcher, C, F)
        if args.stopOnFirst:
            endProgram()
            
    C += searcher.step()
