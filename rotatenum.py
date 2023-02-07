import sys
# M/J2. Arthur Wasserman imagines taking a positive integer
# and moving its last digit to the front. For example 1,234 would
# become 4,123. Wasserman wants to know: What is the smallest
# positive integer such that when you do this, the result is exactly
# double the original?

# note: This uses a more intelligent search than the brute force search
# which searches thru all numbers and is way too slow!

class SolveBase:
    def __init__(self, base, mult, useBruteForce=False):
        if (base > 62):
            print('base not supported:', base)
            sys.exit(-1)
        if (mult >= base):
            print('mult must be less than base', mult, base)
            sys.exit(-1)
        self.base = base
        self.mult = mult
        self.useBruteForce = useBruteForce
        self.bruteExpLimit = 8
        self.verbose = False
        
    # generate the string for the number in the base we are using
    def toStr(self, n):
        convertString = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        str = ''
        while n != 0:
            d = n % self.base
            n = n // self.base
            str = convertString[d] + str
            # print(d, n, str)
        # done, return result string
        return str

    def toInt(self, str):
        return int(str, self.base)

    def className(self):
        return type(self).__name__
    
    def paramStr(self):
        return(f'class {self.className()}, base {self.base}, mult {self.mult}, useBruteForce={self.useBruteForce}')

    def getMinSolution(self):
        self.minval = 0
        self.gaveWarning = False
        if self.useBruteForce:
            self.minval = self.getMinSolutionBruteForce()
        else:
            self.minval = self.getMinSolutionSmart()
        # we finished all the start values show which had the minimum:
        if self.minval == 0:
            print(f' no solutions found for {self.paramStr()}')
            return 0
        else:
            minrot = self.rotated(self.minval)
            print(f'min for {self.paramStr()}: ', end='')
            self.showSolDetail(self.minval, minrot)
            return self.minval

    # by default, there is no "smart" solution unless overridden in child
    def getMinSolutionSmart(self):
        print(f'Smart Solution not supported in class {self.className()}') 
        return 0
    
    def getMinSolutionBruteForce(self):
        self.minval = 0
        # numbers to test, we can skip values that would increase the number of digits
        exp=1
        print(f'exp=', end='')
        while exp < self.bruteExpLimit:
            print(f'{exp} ', end='')
            sys.stdout.flush()
            for n in range(self.base**exp, self.base**(exp+1)//self.mult):
                if n * self.mult == self.rotated(n):
                    return n
            exp = exp + 1
        print('')
        return 0

    def showSolDetail(self, a, r):
        astrlen = len(self.toStr(a))
        print(f'{self.toStr(a)} * {self.mult} = {self.toStr(r)} ({astrlen})')

class SolveRotate(SolveBase):
    def __init__(self, base, mult, rotateamt=1, useBruteForce=False):
        super(SolveRotate, self).__init__(base, mult, useBruteForce)
        self.rotateamt = rotateamt

    def paramStr(self):
        return(f'{super(SolveRotate, self).paramStr()}, rotateamt={self.rotateamt}')
        
    def getMinSolutionSmart(self):
        self.minval = 0
        for start in range(1, self.base**self.rotateamt):
            if (self.verbose):
                print(f'base={self.base}, mult={self.mult}, start={start}')
            a = self.getSolutionForStart(start)
            if a != -1:
                # we got a value of a which might be valid, check if it really is the correct multiple
                r = self.rotated(a)
                if self.verbose:
                    print(f'   a={self.toStr(a)}')
                    print(f'   r={self.toStr(r)}')
                    print(f'prod={a*self.mult}')
                if (r == a*self.mult):
                    print(f'start={start}, a={self.toStr(a)}')
                    if self.verbose:
                        print(f'base {self.base}, mult {self.mult}: ', end='')
                        self.showSolDetail(a, r)
                    # record it and continue in case a higher start value yields a smaller value
                    self.minval = a if self.minval == 0 or a < self.minval else self.minval
        return self.minval

    
class SolveRotateRight(SolveRotate):
    # generate the number which is the argument rotated the correct amount to the right
    def rotated(self, n):
        nstr = self.toStr(n)
        sliceamt = len(nstr) - self.rotateamt
        first = nstr[0:sliceamt]
        second = nstr[sliceamt:]
        result = second + first
        return self.toInt(result)

    def checkForStartMatch(self, start, d, a, exp):
        testa = a + d*self.base**exp
        # iterate thru possible maskshifts
        for maskshift in range(0, self.rotateamt): 
            if testa // self.base**(exp - maskshift) % (self.base**self.rotateamt) == start:
                retval = testa % self.base**(exp - maskshift)
                # print(f'start match, exp={exp}, maskshift={maskshift}, d={self.toStr(d)}, a={self.toStr(a)}, start={self.toStr(start)}, retval={self.toStr(retval)}')
                return retval
        # return 0 if can't find a match
        return 0

    def getSolutionForStart(self, start):
        d = start
        carry = 0
        a = 0
        exp = 0
        while True:
            a = a + (d * self.base**exp)
            # print(f'exp={exp}, a={self.toStr(a)}')
            # compute next d
            d = d * self.mult + carry
            carry = d // self.base**self.rotateamt
            d = d % self.base**self.rotateamt
            exp = exp + self.rotateamt
            # avoid an endless loop
            if exp > self.base**self.rotateamt * self.mult:
                return -1
            # print(f'exp={exp}, d={self.toStr(d)}, carry={carry}  ')
            # if we get back to start with carry==0, we're good
            if carry == 0:
                newa = self.checkForStartMatch(start, d, a, exp) 
                if newa != 0:
                    return newa

class SolveRotateLeft(SolveRotate):
    # generate the number which is the argument rotated the correct amount to the left
    def rotated(self, n):
        nstr = self.toStr(n)
        first = nstr[0:self.rotateamt]
        second = nstr[self.rotateamt:]
        result = second + first
        return self.toInt(result)
    
    def finishSolution(self, curstr, carryin, start):
        if self.verbose:
            print(f'curstr={curstr}, carryin={carryin}, start={start}')
        if (len(curstr) > self.base * self.mult):
            return -1
        lastdchr = curstr[-1]
        #detect stuck in a series of repeating digits
        if (len(curstr) > 3) and curstr[-2] == lastdchr and curstr[-3] == lastdchr and curstr[-4] == lastdchr:
            return -1
        lastd = self.toInt(curstr[-self.rotateamt:])
        nextd = self.mult * lastd
        nextdcarry = nextd // self.base
        if (nextdcarry != carryin):
            return -1
        nextd = nextd % self.base
        if self.verbose:
            print(f'nextd={nextd}, nextdcarry={nextdcarry}')
        if nextd == start:
            return self.toInt(curstr)
        for testcarry in range(0, self.mult):
            if nextd + testcarry > self.base:
                next
            newcurstr = curstr + self.toStr(nextd + testcarry) 
            result = self.finishSolution(newcurstr, testcarry, start)
            if result == -1:
                next
            else:
                return result
        # if we got this far without returning, failure
        return -1

    def getSolutionForStart(self, start):
        # for now only support rotateamt==1
        if (self.rotateamt != 1):
            if not self.gaveWarning:
                print(f'Warning: RotateLeftSmart does not support rotateamt={self.rotateamt}')
                self.gaveWarning = True
            return -1
            # sys.exit(1)
        a = self.finishSolution(self.toStr(start), 0, start)
        return a

class SolveReversed(SolveBase):
    def rotated(self, n):
        nstr = self.toStr(n)
        revstr = "".join(reversed(nstr))
        return self.toInt(revstr)

#-------- main code starts here ---------
if False:
    base = 8
    useRotateRight = True
    rotateChoices = range(1, 4) if useRotateRight else [1]
    showBadCompare = False
    printedRotate = False
    for rotamt in rotateChoices:
        for mult in range(2,base):
            if useRotateRight:
                solver = SolveRotateRight(base, mult, rotamt)
            else:
                solver = SolveReversed(base, mult)
            if not printedRotate:
                n = 4*25 + 3*5 + 2
                print(solver.toStr(n), solver.toStr(solver.rotated(n)))
                printedRotate = True
            resultSmart = solver.getMinSolution()
            solver.useBruteForce = True
            resultBrute = solver.getMinSolution()
            if (resultSmart != resultBrute and showBadCompare):
                print(f'Results Differ: smart={solver.toStr(resultSmart)}, brute={solver.toStr(resultBrute)}')
    sys.exit(1)

rotateamt = 1
for base in range(2, 11):
    for mult in range(2, base):
        solver = SolveRotateRight(base, mult, rotateamt)
        solver.getMinSolution()
