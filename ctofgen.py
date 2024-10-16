import collections
import sys
import argparse
import math
# import numpy

# just some brute force searches for various patterns


def parse_args():
    parser = argparse.ArgumentParser(description='C to F brute force searcher')
    parser.add_argument('--low', type=int, default=1, help='low val for search')
    parser.add_argument('--high', type=int, default=100000, help='high val for search')
    parser.add_argument('--stopOnFirst', default=False, action='store_true', help='whether to stop on first solution')
    parser.add_argument('--test', default=False, action='store_true', help='just test some target generators')
    parser.add_argument('--searcher', default='ShuffleDigits', help='searcher class to use')

    return parser.parse_args()

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)    


class SearcherBase:
    def __init__(self):
        self.tries = 0
        self.matches = 0

    def endProgram(self):
        matchWordEnd = '' if self.matches == 1 else 'es'
        print(f'{self.matches} match{matchWordEnd} out of {self.tries} tries')
        sys.exit(0)
    
    # return 1, 0, or -1
    def signof(self, x):
        return (x > 0) - (x < 0)

    def isMatch(self, C, F):
        # print(C, F, self.targetNumber(C))
        return F == self.targetNumber(C)

    def nextC(self, C):
        return C + self.step()

    def advanceToModStart(self, C):
        while C % 10 not in searcher.modStartList():
            C += 1
        return C

    def cToF(self, C):
        return 9*C//5 + 32

    def fToC(self, F):
        return (F-32)*5 // 9

    # default step and modStartList allow any C ending in 0 or 50
    def step(self):
        return 5

    def modStartList(self):
        return [0,5]

    # utility routine when F high has a certain requirement
    def nextCforHighFReq(self, C, highFReq):
        # for cases where F high digit must be a certain value
        # if F is too big, make big adjustment
        F = self.cToF(C)
        numlen = len(str(abs(F)))
        # get highest digit
        pow10 = (10 ** (numlen-1))
        highestDigitF = abs(F) // pow10
        
        if C > 0 and highestDigitF > highFReq:
            newF = pow10 * 10 * highFReq
            newC =  searcher.fToC(newF) - 10
            newC = self.advanceToModStart(newC)
            # print(C, F, newC, self.cToF(newC))
            return newC
        else:
            return C + self.step()

# class which requires Clow and Fhigh to be 5    
class SearcherBaseCLowFHigh5(SearcherBase):    
    def step(self):
        return 10

    def modStartList(self):
        return [5]

    def nextC(self, C):
        return self.nextCforHighFReq(C, 5)
    
    
class ShuffleDigits(SearcherBase):
    def isMatch(self, C, F):
        counterF = collections.Counter(list(str(F)))
        counterC = collections.Counter(list(str(C)))
        return counterF == counterC
    
class ReverseDigits(SearcherBaseCLowFHigh5):
    def targetNumber(self, number):
        sgn = self.signof(number)
        absnum = abs(number)
        numList = list(str(absnum))
        reversedNum = int(''.join(numList[::-1]))
        return reversedNum * sgn
    
class RotateRight(SearcherBaseCLowFHigh5):
    def targetNumber(self, number):
        sgn = self.signof(number)
        absnum = abs(number)
        numlen = len(str(absnum))
        # get lowest digit
        lowest = absnum % 10
        return (absnum // 10 + lowest * (10 ** (numlen-1))) * sgn
    
class RotateLeft(SearcherBase):
    def targetNumber(self, number):
        sgn = self.signof(number)
        absnum = abs(number)
        numlen = len(str(absnum))
        # get highest digit
        pow10 = (10 ** (numlen-1))
        highest = absnum // pow10
        return ((absnum % pow10)  * 10 + highest) * sgn
    
class SwapFirstLast(SearcherBaseCLowFHigh5):
    def targetNumber(self, number):
        sgn = self.signof(number)
        absnum = abs(number)
        numList = list(str(absnum))
        tmp = numList[0]
        numList[0] = numList[-1]
        numList[-1] = tmp
        swappedNum = int(''.join(numList))
        return swappedNum * sgn
    

# main code:
        
args = parse_args()
if args.low < -273.15:
    print("low value adjusted to absolute 0 (-273 C)")
    args.low = -273
if args.test:
    for S in [RotateLeft(), RotateRight(), ReverseDigits(), SwapFirstLast()]:
        print(S)
        for tst in [1234, 12345, 123450, 12345678901234567890]:
            for x in [tst, -1*tst]:
                print(x, S.targetNumber(x))
    sys.exit(0)
    
searcher = str_to_class(args.searcher)()
C = args.low
# advance until C meets the modstart requirement
C = searcher.advanceToModStart(C)

while C < args.high:
    searcher.tries += 1
    if searcher.tries % 1000000 == 0:
        print(f'...{searcher.tries}\r', end='')
    #if C % 1000 in searcher.modStartList():
    #    print(f'{C}...')
    F = searcher.cToF(C)
    if searcher.isMatch(C, F):
        searcher.matches += 1
        print(args.searcher, C, F)
        if args.stopOnFirst:
            break
            
    C = searcher.nextC(C)


searcher.endProgram()
