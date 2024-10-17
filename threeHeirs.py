import collections
import sys


# puzzle statement
# Three Heirs (contributed by Kaustuv Sengupta )
       #        A wealthy man had three adult children all of whom were
       # skilled at math and logic. To get a share of his inheritance
       # each had to correctly determine a secret number which he had
       # chosen. He told them that the number had four different
       # non-zero decimal digits, in ascending order.  He prepared three
       # sealed envelopes each of which contained a clue. Envelope #1
       # contained the product of the four digits, envelope #2 contained
       # the sum of the squares of the four digits, and envelope #3
       # contained the sum of the product of the first two digits and
       # the product of the last two digits. For example, if the number
       # were 1234, the first envelope would contain 1×2×3×4=24, the
       # second envelope would contain 12+22+32+42=30, and the third
       # envelope would contain 1×2+3×4=14. The envelopes were clearly
       # marked. Each child was given one envelope. They each saw the
       # number inside their own envelopes but could not see the numbers
       # inside the other two envelopes.  Then he explained the
       # rules. After one hour each child could either submit a number
       # or decline. Anyone who submitted a wrong answer would be
       # eliminated and get nothing. If one or more submitted the
       # correct answer they would receive equal shares of the
       # inheritance. The contest would then end, with the others
       # getting nothing. If no one submitted the correct answer they
       # would be instructed to work on the problem for another
       # hour. The process would repeat as often as necessary. Each of
       # the children decided not to submit an answer unless they sure
       # it was correct.  The children were placed in different rooms
       # where they could not communicate with one another. At the end
       # of the first hour no one had submitted an answer. At the end of
       # the second hour no one had submitted an answer. At the end of
       # the third hour no one had submitted an answer. At the end of
       # the fourth hour all three of them submitted the correct answer!
       # What number had the father chosen?

debug = False

def dbglog(s):
    if debug:
        print(s)
        
class NumInfo:
    def __init__(self, a, b, c, d):
        self.num = a*1000 + b*100 + c*10 +d
        self.prod = a * b * c * d
        self.sumsq = a**2 + b**2 + c**2 + d**2
        self.sumprod = a*b + c*d
        prodDict.addToDict(self.prod, self)
        sumsqDict.addToDict(self.sumsq, self)
        sumprodDict.addToDict(self.sumprod, self)

    def __str__(self):
        return f'{self.num}: {self.prod}  {self.sumsq}  {self.sumprod}'


class MyDict:
    def __init__(self, name):
        self.mydict = {}
        self.reverseDict = {}
        self.name=name

    def addToDict(self, key, info):
        if key in self.mydict:
            self.mydict[key].append(info)
        else:
            self.mydict[key] = [info]
        self.reverseDict[info.num] = key

    def infoListStr(self, infoList):
        str = ''
        if len(infoList) == 0:
            str += '[]'
        else:
            str += '['
            for info in infoList:
                str += f'{info.num} '
            str += ']'
        return str
    
        
    def removeNum(self, key, num):
        # dbglog(f'{self.name}: removeNum {key} {num}')
        if not key in self.mydict:
            dbglog(f' ...could not find key={key} in {self.name}')
            return
        for idx in range(0, len(self.mydict[key])):
            # dbglog(f'{self.name}: removeNumid {key} {num} {idx} {self.mydict[key][idx].num}')
            if self.mydict[key][idx].num == num:
                del self.mydict[key][idx]
                # if shortened list is down to length 0, remove mapping
                if len(self.mydict[key]) == 0:
                    del self.mydict[key]
                    dbglog(f' {self.name} removing {key}->{num}')
                    return
                else:
                    dbglog(f' {self.name} shortening list for {key} to {self.infoListStr(self.mydict[key])}')
                    return
        dbglog(f'  {self.name} did not match {num} in list for {key}')
        return
        # if we got this far, list exists but num is not in it, just return
        dbglog(f' for key {key}, {num} not found in list')
        return
                        
    def buildLen1KeyDict(self):
        # builds key to info mapping
        len1dict = {}
        for key in self.mydict:
            if len(self.mydict[key]) == 1:
                len1dict[key] = self.mydict[key][0]
        self.len1KeyDict = len1dict
        return len1dict
                
        
    def removeFromAll3(self, key, info, prodDict, sumsqDict, sumprodDict):
        num = info.num
        dictKeys = ((prodDict, info.prod), (sumsqDict, info.sumsq), (sumprodDict, info.sumprod))
        for (remdict, key) in dictKeys:
            #if num == 3578:
            #    print(f'{remdict.name}, {key}, {num}')
            #    print(dictKeys)
            remdict.removeNum(key, num)
            #if key == 840:
            #    print(f'finished {remdict.name} {key}')
    def show(self):
        print(f'{self.name}:')
        for key in self.mydict:
            print(f'key={key}: [', end="")
            ary = self.mydict[key]
            for info in ary:
                print(f'{info.num} ', end="")
            print(']')


def checkForSameLen1InDicts(dicts):
    prodDict, sumsqDict, sumprodDict = dicts

    for key, info in prodDict.len1KeyDict.items():
        num = info.num
        count = 1
        for otherdict in [sumsqDict, sumprodDict]:
            for othkey, othinfo in otherdict.len1KeyDict.items():
                othnum = othinfo.num
                if othnum == num:
                    count += 1
                    # print(f' match for {othnum} in {otherdict.name}, count={count}, adict={adict.name}') 
                    break
        if count == 3:
            print(f' {num} seen in all 3 len1 dicts')
    
prodDict = MyDict('prodDict')
sumsqDict = MyDict('sumsqDict')
sumprodDict = MyDict('sumprodDict')
dicts = [prodDict, sumsqDict, sumprodDict]


for a in range(1,10):
    for b in range(a+1, 10):
        for c in range(b+1, 10):
            for d in range(c+1, 10):
                info = NumInfo(a,b,c,d)
                # sys.exit(0)
                # print(f'{a}{b}{c}{d}   {prod:4d}  {sumsq:4d}  {sumprod:4d}')

# we know that no one's original number was a len1
# so for each len1 entry, we can remove it from each of the three dicts
for n in range(1, 6):
    print(f'End of hour {n}')
    for adict in dicts:
        adict.buildLen1KeyDict()
        dbglog(f'{adict.name} len1KeyDict len: {len(adict.len1KeyDict)}')
    for adict in dicts:
        adict.show()
    checkForSameLen1InDicts(dicts)
        
    for adict in dicts:
        # for each dict, go thru and find any len 1 items
        # and remove them from all 3 dicts
        for key, info in adict.len1KeyDict.items():
            dbglog(f'{adict.name} len1List to remove {key}->{info.num}')
            adict.removeFromAll3(key, info, prodDict, sumsqDict, sumprodDict)

