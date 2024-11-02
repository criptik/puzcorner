import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='str pattern matcher')
    parser.add_argument('--file', type=str, help='file to read from')
    parser.add_argument('--matcher', default='Matcher2Consec', help='matcher class to use')

    return parser.parse_args()

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)    

class Matcher:
    def strsMeetCriteria(self, stra, strb):
        diffs = []
        for n in range(0, len(stra)):
            if stra[n] != strb[n]:
                if len(diffs) >= self.maxDiffs():
                    return False
                else:
                    diffs.append(n)
                
        if len(diffs) < self.minDiffs():
            return False

        return self.checkDiffs(diffs)

    
    def maxDiffs(self):
        pass

    def minDiffs(self):
        pass


class Matcher1(Matcher):
    def maxDiffs(self):
        return 1

    def minDiffs(self):
        return 1

    def checkDiffs(self, diffs):
        return True
    

class Matcher2Any(Matcher):
    def maxDiffs(self):
        return 2

    def minDiffs(self):
        return 2

    def checkDiffs(self, diffs):
        return True

class Matcher2Consec(Matcher2Any):
    def checkDiffs(self, diffs):
        return diffs[1] == diffs[0] + 1
    
class Matcher2NonConsec(Matcher2Any):
    def checkDiffs(self, diffs):
        return diffs[1] != diffs[0] + 1


class Matcher3Any(Matcher):
    def maxDiffs(self):
        return 3

    def minDiffs(self):
        return 3

    def checkDiffs(self, diffs):
        return True
    
class Matcher3Consec(Matcher3Any):
    def checkDiffs(self, diffs):
        return diffs[2] == diffs[0] + 2
    

args = parse_args()

strList = []
with open(args.file) as file:
    for line in file:
        strList.append(line.lstrip().rstrip().upper())

lenmap = {}

for c in strList:
    siz = len(c)
    if siz not in lenmap.keys():
        lenmap[siz] = [c]
    else:
        lenmap[siz].append(c)

matcher = str_to_class(args.matcher)()

for siz in sorted(lenmap.keys()):
    # print(f'---{siz}---')
    ary = lenmap[siz]
    for j in range(0, len(ary)):
        for k in range(j+1, len(ary)):
            jc = ary[j]
            kc = ary[k]
            if matcher.strsMeetCriteria(jc, kc):
                print(jc, kc)
    
