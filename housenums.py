# Formula is 2*N**2 = S(S+1)
# N = Alice's #
# S = total on street
# S**2 + S - 2*N**2 = 0
# roots = (-1 +- sqrt(1+4*2*N**2)) / 2
import math

lolim = 2
hilim = 10000000


for N in range (lolim, hilim):
    root = math.sqrt(1 + 8 * N**2)
    if root != int(root):
        continue
    S = (root - 1) / 2
    print(f'house {N} out of {int(S)}')
    
    
