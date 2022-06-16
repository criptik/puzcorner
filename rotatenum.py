import sys
# note: the brute force search thru all numbers is way too slow!

class SolveBase:
    def __init__(self, base, mult):
        if (base > 62):
            print('base not supported:', base);
        self.base = base
        self.mult = mult
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
            
class SolveRotateRight(SolveBase):
    def __init__(self, base, mult, rotateamt):
        super(SolveRotateRight, self).__init__(base, mult)
        self.rotateamt = rotateamt
        
    # generate the number which is the argument rotated the correct amount to the right
    def rotated(self, n):
        nstr = self.toStr(n)
        sliceamt = len(nstr) - self.rotateamt
        first = nstr[0:sliceamt]
        second = nstr[sliceamt:]
        result = second + first
        return int(result, self.base)

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

    def showSolDetail(self, a, r):
        astrlen = len(self.toStr(a))
        oddtxt = 'odd length' if (astrlen % 2 == 1) else ''
        print(f'{self.toStr(a)} * {self.mult} = {self.toStr(r)} ({astrlen}) {oddtxt}')

    def getSolution(self):
        minval = 0
        if (self.verbose):
            print('base=', self.base, 'mult=', self.mult, '---------')
        # for start in range(34, 35):
        for start in range(1, self.base**self.rotateamt):
            d = start
            carry = 0
            a = 0
            exp = 0
            lastd = 0
            while True:
                a = a + (d * self.base**exp)
                lastd = d
                # print(f'exp={exp}, a={self.toStr(a)}')
                # compute next d
                d = d * self.mult + carry
                carry = d // self.base**self.rotateamt
                d = d % self.base**self.rotateamt
                exp = exp + self.rotateamt
                # avoid an endless loop
                if exp > self.base**self.rotateamt * self.mult:
                    break
                # print(f'exp={exp}, d={self.toStr(d)}, carry={carry}  ')
                # if we get back to start with carry==0, we're good
                if carry == 0:
                    newa = self.checkForStartMatch(start, d, a, exp) 
                    if newa != 0:
                        a = newa
                        break

            # we got out of loop with some value of a, check if it really is the correct multiple
            r = self.rotated(a)
            if (r == a*self.mult and lastd != 0):
                if self.verbose:
                    print(f'base {self.base}, mult {self.mult}: ', end='')
                    self.showSolDetail(a, r)
                minval = a if minval == 0 or a < minval else minval
            else:
                pass
                # print(f'bad {start}')

        # we finished all the start values show which had the minimum:
        minrot = self.rotated(minval)
        print(f'min for base {self.base}, mult {self.mult}: ', end='')
        self.showSolDetail(minval, minrot)
                


if False:
    solver = SolveRotateRight(16, 2, 2)
    print(solver.toStr(65))
    # print(solver.rotated(12345678))
    # solver.getSolution()
    sys.exit(1)

rotateamt = 1
for base in range(2, 11):
    for mult in range(2, base):
        solver = SolveRotateRight(base, mult, rotateamt)
        solver.getSolution()
