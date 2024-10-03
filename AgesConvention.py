import sys
import math
import argparse


# from MIT News Puzzle Corner, Sep/Oct 2024

# Three Silovian mathematicians, Adal, Biru and Cado meet at an actuarial convention.
# Adal says to the other two, "If you multiply your ages, the product is the year my
# mother was born." Biru says, "If you two multiply your ages, the product is the year
# my mother's mother was born." Cado says, "If you two multiply your ages, the product
# is the year my mother's mother's mother was born." All Silovians know that no Silovian
# woman has ever given birth younger than 15 nor older than 45.
# A fourth mathematician, Diba, arrives and says, "I heard your conversation, but I cannot
# determine any of your ages." Adal says, "We all have different ages."
# Diba says, "I still can't determine the age of any of you."
# What is the most recent year that this convention could have been held?
       
# Note the condition "I still can't determine the age of any of you."
# This means there have to be multiple possible answers for a given year
# and none of a,b,c positions in the answers can be all the same age


def parse_args():
    parser = argparse.ArgumentParser(description='Puzzle Corner Ages Convention Problem')
    parser.add_argument('--high', type=int, default=2024, help='high year for search')
    parser.add_argument('--low', type=int, default=1400, help='low year for search')
    parser.add_argument('--minSolutionsToShow',  type=int, default=2, help='show only years having at least this many solutions')
    parser.add_argument('--noStopOnFirst', default=False, action='store_true', help='show all solutions rather than stop at first one')
    parser.add_argument('--showPartialSolvable', default=False, action='store_true', help='require only 1 of a,b,c to be unsolvable instead of all 3 (breaks [uzzle statement)')
    parser.add_argument('--allowDuplicateAges', default=False, action='store_true', help='allow solutions where a,b,c can have duplicate ages (breaks puzzle statement )')
    
    return parser.parse_args()


class Guess:
    def __init__(self, curYear, a, b, c, genMap):
        self.curYear = curYear
        self.abc = [a,b,c]
        self.aAncAge = curYear - b*c
        self.bAncAge = curYear - a*c
        self.cAncAge = curYear - a*b
        self.genMap = genMap

    def checkAncestryForGenMap(self, answers):
        agen, bgen, cgen = genMap
        a, b, c = self.abc
        if (couldBeAncestor (a, self.aAncAge, agen)
            and couldBeAncestor (b, self.bAncAge, bgen)
            and couldBeAncestor (c, self.cAncAge, cgen)):
            # map ordered a,b,c to abcMapped based on genMap
            self.setabcMapped()
            return True
        else:
            return False
        
        
    def setabcMapped(self):
        self.abcMapped = [0, 0, 0]
        for idx in range(0, 3):
            self.abcMapped[self.genMap[idx]-1] = self.abc[idx]

        
    def print(self):
        a,b,c = self.abcMapped
        aAncBorn = b*c
        bAncBorn = a*c
        cAncBorn = a*b
        aAncAge = self.curYear - aAncBorn
        bAncAge = self.curYear - bAncBorn
        cAncAge = self.curYear - cAncBorn
        print(f'     {a} {b} {c}    {aAncBorn:4}/{aAncAge:3}/{(aAncAge-a):3}  {bAncBorn:4}/{bAncAge:3}/{(bAncAge-b):3}  {cAncBorn:4}/{cAncAge:3}/{(cAncAge-c):3}   {self.genMap}')
        
class AnswerList:
    def __init__(self):
        self.answers = []

    def length(self):
        return len(self.answers)
    
    def append(self, guess):
        self.answers.append(guess)
        
    def alreadyContains(self, guess):
        for ans in self.answers:
            if ans.abcMapped == guess.abcMapped:
                return True
        return False

    def meetsSolvableReqs(self, args):
        # special case if user wants years with single answers
        if len(self.answers) == 1:
            return True
        # normal case
        # count the number of positions where all the answer parts are the same
        allSameCount = 0
        for posidx in range(0, 3):
            posAnswers = []
            for ans in self.answers:
                posAnswers.append(ans.abcMapped[posidx])
            if allSame(posAnswers):
                allSameCount += 1
        if args.showPartialSolvable:
            return allSameCount != 3
        else: 
            return allSameCount == 0

    def print(self):
        for ans in self.answers:
            ans.print()
        
    
def finishProgram(tries):
    print(f'{tries} tries')
    sys.exit(0)

def couldBeAncestor(myAge, ancAge, gencount):
    return gencount*15 <= ancAge-myAge <= gencount*45

def hasDuplicates(seq):
    return len(seq) != len(set(seq))

def allSame(seq):
    return len(set(seq)) == 1


args = parse_args()
tries = 0
# for trying the different mappings of generations 1,2,3
genMapList = [[1,2,3], [1,3,2], [2,3,1], [2,1,3], [3,2,1], [3,1,2]]

# minSolutions==1 is special case, allow partial solvable for > 1 as well
if args.minSolutionsToShow == 1:
    args.showPartialSolvable = True
    
# the main loop
for curYear in range(args.high, args.low, -1):
    answers = AnswerList()
    if curYear % 100 == 0:
        print(curYear)
    buf = ''
    # all 3 a,b,c have different ages so assume a < b < c
    # and we will pick c first and use negative step on each of c,b,a
    # note: the way they map to ancestors will be tested later 
    # for now, have to try all 6 permutations although it always seems to come out [1,2,3]
    # once c is selected, b is limited to at most curYear/c, and a is limited to at most b-1
    # limits for range of c: rough start is 1 < c < curYear/2
    # since even if a=1 and b=2, c*b < curYear
    # what is maximum difference allowed between c and b?
    # a is at most b-1  and (curYear-a*b) - c must be > 15 and < 135
    # So once b gets to the point that curYear-(b*(b-1)) - c < 135, we might as well stop searching the rest of the b
    # similarly when a gets small enough that curYear-(b*a) - c < 135
    
    for c in range(1+math.floor(curYear/2), 1, -1):
        bmax1 = c-1 if not args.allowDuplicateAges else c
        bmax = min(math.floor(curYear/c), bmax1)
        for b in range(bmax, 1, -1):
            amax = b-1 if not args.allowDuplicateAges else b
            if (curYear - (b * amax)) - c > 135:
                break
            for a in range(amax, 1, -1):
                if (curYear - (b * a)) - c > 135:
                    break
                # create the Guess object
                for genMap in genMapList:
                    guess = Guess(curYear, a, b, c, genMap)
                    # check ancestry limits and add to answers if ok
                    tries = tries + 1
                    # debugging breakpoint
                    # if curYear >= 2023 and a == 43 and b==44 and c==44 and genMap == [1,2,3]:
                    #    print('Break')
                    if guess.checkAncestryForGenMap(answers):
                        if not answers.alreadyContains(guess):
                            answers.append(guess)


    # finished with loop for this year, check total accumulated answers
    # debugging
    # if curYear == 1457:
    #    print('Break')
    if answers.length() >= args.minSolutionsToShow and answers.meetsSolvableReqs(args):
        print(f'{curYear}: {answers.length()} Solutions')
        answers.print()
        if not args.noStopOnFirst:
            finishProgram(tries)

finishProgram(tries)
