import sys
# note: the brute force search thru all numbers is way too slow!

class SolveBase:
    def __init__(self, base, mult):
        if (base > 62):
            print('base not supported:', base);
        self.base = base
        self.mult = mult

    # generate the string for the number in the base we are using
    def toStr(self, n):
        convertString = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        if n < self.base:
            return convertString[n]
        else:
            return self.toStr(n//self.base) + convertString[n%self.base]

class SolveRotateRight(SolveBase):
    # generate the number which is the argument rotated the correct amount to the right
    def rotated(self, n):
        nstr = self.toStr(n)
        sliceamt = len(nstr) - self.rotateamt
        first = nstr[0:sliceamt]
        second = nstr[sliceamt:]
        result = second + first
        return int(result, self.base)


class SolveRotateRightOne(SolveRotateRight):
    def __init__(self, base, mult):
        super(SolveRotateRightOne, self).__init__(base, mult)
        self.rotateamt=1
        
    def getSolution(self):
        print('base=', self.base, 'mult=', self.mult, '---------')
        for start in range(1, self.base):
            d = start
            a = 0
            carry = 0
            a = d
            exp = 1
            lastd = 0
            while True:
                d = d * self.mult + carry
                carry = d // self.base
                d = d % self.base
                # print(exp, d, carry, '  ', end='')
                # if we get back to start with carry==0, we're good
                if d == start and carry == 0:
                    break
                # avoid an endless loop
                if exp > self.base * self.mult:
                    break
                a = a + d*self.base**exp
                lastd = d
                # print(self.toStr(a))
                exp = exp + 1

            r = self.rotated(a)

            if (r == a*self.mult and lastd != 0):
                print(f'ok  {start} {self.toStr(a)} {self.toStr(r)} ({len(self.toStr(a))})')
            else:
                print(f'bad {start}')

class SolveRotateRightTwo(SolveRotateRight):
    def __init__(self, base, mult):
        super(SolveRotateRightTwo, self).__init__(base, mult)
        self.rotateamt=2
        
    def checkForStartMatch(self, start, d, a, exp):
        testa = a + d*self.base**exp
        if testa // self.base**exp % (self.base**2) == start:
            retval = testa % self.base**exp
            # print(f'saw full-d succeed, exp={exp}, d={self.toStr(d)}, a={self.toStr(a)}, start={self.toStr(start)}, retval={self.toStr(retval)}')
            return retval
        if testa // self.base**(exp-1) % (self.base**2) == start:
            retval = testa % self.base**(exp-1)
            # print(f'saw half-d succeed, exp={exp}, d={self.toStr(d)}, a={self.toStr(a)}, start={self.toStr(start)}, retval={self.toStr(retval)}')
            return retval
        return 0
        
    def getSolution(self):
        print('base=', self.base, 'mult=', self.mult, '---------')
        # for start in range(34, 35):
        for start in range(1, self.base**2):
            d = start
            carry = 0
            a = 0
            exp = 0
            lastd = 0
            while True:
                a = a + d*self.base**exp
                lastd = d
                # print(f'exp={exp}, a={self.toStr(a)}')
                # compute next d
                d = d * self.mult + carry
                carry = d // self.base**2
                d = d % self.base**2
                exp = exp + 2
                # avoid an endless loop
                if exp > self.base**2 * self.mult:
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
                astrlen = len(self.toStr(a))
                oddtxt = 'odd length' if (astrlen % 2 == 1) else ''
                print(f'ok  base={self.base}, start={self.toStr(start)} {self.toStr(a)} * {self.mult} = {self.toStr(r)} ({astrlen}) {oddtxt}')
            else:
                pass
                # print(f'bad {start}')



if False:
    solver = SolveRotateRightTwo(10, 2)
    print(solver.rotated(12345678))
    # solver.getSolution()
    sys.exit(1)

for base in range(3, 11):
    for mult in range(2, base):
        # solver = SolveRotateRightOne(base, mult)
        solver = SolveRotateRightTwo(base, mult)
        solver.getSolution()
