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

class Answer:
    def __init__(self, a, b, c, genMap):
        self.abc = [a,b,c]
        self.genMap = genMap

    def print(self):
        a,b,c = self.abc
        cAncBorn = a*b
        bAncBorn = a*c
        aAncBorn = b*c
        aAncAge = curYear - aAncBorn
        bAncAge = curYear - bAncBorn
        cAncAge = curYear - cAncBorn
        print(f'     {a} {b} {c}    {aAncBorn:4}/{aAncAge:3}/{(aAncAge-a):3}  {bAncBorn:4}/{bAncAge:3}/{(bAncAge-b):3}  {cAncBorn:4}/{cAncAge:3}/{(cAncAge-c):3}   {self.genMap}')
        

        
def isInAnswers(answers, a, b, c):
    for ans in answers:
        if ans.abc == [a,b,c]:
            return True
    return False

    
def parse_args():
    parser = argparse.ArgumentParser(description='Puzzle Corner Ages Convention Problem')
    parser.add_argument('--high', type=int, default=2024, help='high year for search')
    parser.add_argument('--low', type=int, default=1400, help='low year for search')
    parser.add_argument('--minSolutionsToShow',  type=int, default=2, help='show only years having at least this many solutions')
    parser.add_argument('--noStopOnFirst', default=False, action='store_true', help='show all solutions rather than stop at first one')
    parser.add_argument('--singleGenMap', default=False, action='store_true', help='use only [1,2,3] as the genMap (breaks rules)')
    parser.add_argument('--showPartialSolvable', default=False, action='store_true', help='require only 1 of a,b,c to be unsolvable instead of all 3 (breaks rules)')
    parser.add_argument('--allowDuplicateAges', default=False, action='store_true', help='allow solutions where a,b,c can have duplicate ages (breaks rules)')
    
    return parser.parse_args()

def finishProgram(tries):
    print(f'{tries} tries')
    sys.exit(0)

def couldBeAncestor(myAge, ancAge, gencount):
    return gencount*15 <= ancAge-myAge <= gencount*45

def abcOrderedByGenMap(a, b, c, genMap):
    abcBySize = [a, b, c]
    abcByGenMap = [0, 0, 0]
    for idx in range(0, 3):
        abcByGenMap[genMap[idx]-1] = abcBySize[idx]
    return abcByGenMap

def hasDuplicates(seq):
    return len(seq) != len(set(seq))

def allSame(seq):
    return len(set(seq)) == 1

def meetsSolvableReqs(args, answers):
    # special case if user wants years with single answers
    if len(answers) == 1:
        return True
    # normal case
    # count the number of positions where all the answer parts are the same
    allSameCount = 0
    for posidx in range(0, 3):
        posAnswers = []
        for ans in answers:
            posAnswers.append(ans.abc[posidx])
        if allSame(posAnswers):
            allSameCount += 1
    if args.showPartialSolvable:
        return allSameCount != 3
    else: 
        return allSameCount == 0

args = parse_args()
tries = 0
# for trying the different mappings of generations 1,2,3
if args.singleGenMap:
    genMapList = [[1,2,3]]
else:
    genMapList = [[1,2,3], [1,3,2], [2,3,1], [2,1,3], [3,2,1], [3,1,2]]
    # print(args, genMapList)
    # sys.exit(0)

# minSolutions==1 is special case, allow partial solvable for > 1 as well
if args.minSolutionsToShow == 1:
    args.showPartialSolvable = True
    
# the main loop
for curYear in range(args.high, args.low, -1):
    answers = []
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
    
    for c in range(math.floor(curYear/2), 1, -1):
        bmax1 = c-1 if not args.allowDuplicateAges else c
        bmax = min(math.floor(curYear/c), bmax1)
        for b in range(bmax, 1, -1):
            amax = b-1 if not args.allowDuplicateAges else b
            if (curYear - (b * amax)) - c > 135:
                break
            for a in range(amax, 1, -1):
                if (curYear - (b * a)) - c > 135:
                    break
                # print(a,b,c)
                cAncBorn = a*b
                bAncBorn = a*c
                aAncBorn = b*c
                aAncAge = curYear - aAncBorn
                bAncAge = curYear - bAncBorn
                cAncAge = curYear - cAncBorn
                
                for genMap in genMapList:
                    agen, bgen, cgen = genMap
                    tries = tries + 1
                    # debugging breakpoint
                    # if curYear >= 2023 and a == 43 and b==44 and c==44 and genMap == [1,2,3]:
                    #    print('Break')
                    if (couldBeAncestor (a, aAncAge, agen)
                        and couldBeAncestor (b, bAncAge, bgen)
                        and couldBeAncestor (c, cAncAge, cgen)):
                        # map ordered a,b,c to real a,b,c based on genMap
                        aMap, bMap, cMap = abcOrderedByGenMap(a, b, c, genMap)
                        if not isInAnswers(answers, aMap, bMap, cMap):
                            answers.append(Answer(aMap, bMap, cMap,genMap))
                             
    if len(answers) >= args.minSolutionsToShow and meetsSolvableReqs(args, answers):
        print(f'{curYear}: {len(answers)} Solutions')
        for ans in answers:
            ans.print()
        if not args.noStopOnFirst:
            finishProgram(tries)

