# Formula is 2*N**2 = S(S+1)
# N = Alice's #
# S = total on street
# S**2 + S - 2*N**2 = 0
# so given S
# 2*N**2 = S**2 + S
# N = sqrt((S**2 + S) / 2)

# to speed things up we note that either S or S+1 must be an odd square
# using this logic
# (S * (S + 1)) / 2  has to be an integer squared
# We know one of N and N+1 is even and odd
# assume neither N nor N+1 is a square
# then one of them will have a factor x >= 3 which is not a factor of the other

# Now assume the even one is a square.  Then again the odd will have a
# factor x >= 3 which is not a factor of the other.

# Thus one of N and N+1 must be an odd square.

import math
import gmpy2

lolim = 3
hilim = 10000000


for oddnum in range (lolim, hilim, 2):
    oddsq = oddnum*oddnum
    for fix in [1, -1]:
        evensqdoub = oddsq + fix
        evensq = evensqdoub // 2
        if not gmpy2.is_square(evensq):
            continue
        evennum = math.isqrt(evensq)
        root = oddnum * evennum
        N = root
        S = min(oddsq,evensqdoub)
        print(f'house {N:,d} out of {S:,d}')
        break
    
    
