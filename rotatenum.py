import sys
# note: the brute force search thru all numbers is way too slow!

base = 0
mult = 0

def toStr(n,abase):
    convertString = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    if n < abase:
        return convertString[n]
    else:
        return toStr(n//abase,abase) + convertString[n%abase]
    
def rotated(a):
    return a // base + a%base * base**(len(toStr(a, base)) - 1)

for base in range(2,16):
    for mult in range(2, base):
        print('base=', base, 'mult=', mult, '---------')
        for start in range(1, base):
            d = start
            a = 0
            carry = 0
            a = d
            exp = 1
            lastd = 0
            while True:
                d = d * mult + carry
                carry = d // base
                d = d % base
                # print(exp, d, carry, '  ', end='')
                # if we get back to start with carry==0, we're good
                if d == start and carry == 0:
                    break
                # avoid an endless loop
                if exp > base * mult:
                    break
                a = a + d*base**exp
                lastd = d
                # print(toStr(a,base))
                exp = exp + 1

            r = rotated(a)

            if (r == a*mult and lastd != 0):
                print('ok ', start, toStr(a,base), toStr(r, base), len(toStr(a, base)))
            else:
                print('bad', start, toStr(a,base), toStr(r, base))
