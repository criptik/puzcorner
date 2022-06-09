import sys
# M/J2. Arthur Wasserman imagines taking a positive integer
# and moving its last digit to the front. For example 1,234 would
# become 4,123. Wasserman wants to know: What is the smallest
# positive integer such that when you do this, the result is exactly
# double the original?

# this brute force test is too slow!

# 3 digit test
# m = 100*a + 10*b + c
# n = 100*c + 10*a + b

# n = 2*m
# so 100*c + 10*a + b = 2*(100*a + 10*b + c)
# so 100*c + 10*a + b = 200*a + 20*b + 2*c
# so 190*a + 19*b = 98*c

# two digits
# m = 10*a + b
# n = 10*b + a
# 20*a + 2*b = 10*b + a
# 19*a = 8*b

# general
# given a list of digits (ones place, tens place, etc)
# compute m
# compute n
# see if 2*m == n

numlen = 7
gap = 12345
count = 0

for m in range(10**(numlen-1), 10**numlen):
    # build ary of digits
    mary = []
    mtmp = m
    for exp in range(0, numlen):
        tenbase = 10
        # print(mtmp, exp, tenbase)
        dig = mtmp % tenbase
        mtmp = mtmp // tenbase
        mary.append(dig)
    nary = mary[1:] + mary[:1]
    n = 0
    for exp in range(0, numlen):
        n = n + nary[exp]*(10**exp)

    count = count + 1
    if (2*m == n):
        print(m, n)
        sys.exit(1)
    if (count % gap == gap-1):
        print(m, n)
        pass
        


