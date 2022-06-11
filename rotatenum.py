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

class SolveRotateRightOne(SolveBase):
    # generate the number which is the argument rotated one to the right
    def rotated(self, n):
        nstr = self.toStr(n)
        sliceamt = len(nstr) - 1
        first = nstr[0:sliceamt]
        second = nstr[sliceamt]
        result = second + first
        return int(result, self.base)

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

class SolveRotateRightTwo(SolveBase):
    # generate the number which is the argument rotated two to the right
    def rotated(self, n):
        nstr = self.toStr(n)
        sliceamt = len(nstr) - 2
        first = nstr[0:sliceamt]
        second = nstr[sliceamt:]
        result = second + first
        return int(result, self.base)

    def getSolution(self):
        print('base=', self.base, 'mult=', self.mult, '---------')
        # for start in range(34, 35):
        for start in range(1, self.base**2):
            d = start
            carry = 0
            a = 0
            exp = 0
            lastd = 0
            # print(f'before loop, exp={exp}, d={d}, carry={carry}  ')
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
                # print(f'exp={exp}, d={d}, carry={carry}  ')
                # if we get back to start with carry==0, we're good
                if d == start and carry == 0:
                    break

            r = self.rotated(a)

            if (r == a*self.mult and lastd != 0):
                print(f'ok  {start} {self.toStr(a)} {self.toStr(r)} ({len(self.toStr(a))})')
            else:
                pass
                # print(f'bad {start}')



if False:
    solver = SolveRotateRightTwo(8, 4)
    solver.getSolution()
    sys.exit(1)

for base in range(3, 11):
    for mult in range(2, base):
        # solver = SolveRotateRightOne(base, mult)
        solver = SolveRotateRightTwo(base, mult)
        solver.getSolution()
