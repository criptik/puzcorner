# Formula is 2*N**2 = S(S+1)
# N = Alice's #
# S = total on street
# S**2 + S - 2*N**2 = 0
# so given S
# 2*N**2 = S**2 + S
# N = sqrt((S**2 + S) / 2)

import math

lolim = 2
hilim = 10000000


for S in range (lolim, hilim):
    root = math.sqrt(S*(S+1)/2)
    if root != int(root):
        continue
    N = int(root)
    print(f'house {N} out of {int(S)}')
    
    
