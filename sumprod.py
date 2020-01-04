import sys
import math
from functools import reduce

def lowfactors(n):    
    return set(reduce(list.__add__, 
                ([i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

numlo = int(sys.argv[1]) if len(sys.argv) >= 2 else 710
numhi = int(sys.argv[2]) if len(sys.argv) >= 3 else 712

for num in range (numlo, numhi):
    count = 0
    finds = 0
    goal = num * 1000000
    # goalfactors = lowfactors(goal)
    n1top = int(goal**0.25) + 1
    # print(num, n1top)
    for n1 in range(1, n1top):
        # print('.', end='')
        if goal % n1 != 0:
            continue
        n2top = int((goal/n1)**0.333) + 1
        for n2 in range(n1, n2top):
            if goal % (n1 * n2) != 0:
                continue
            n3n4sum = num - (n1 + n2)
            n3n4prod = goal // (n1 * n2)
            found = False
            if True:
                rootprod = math.sqrt(n3n4prod)
                for n3 in range(1, int(rootprod) + 1):
                    count = count + 1
                    if n3n4prod % n3 != 0:
                        continue
                    n4 = n3n4prod / n3
                    if n3 >= n2 and n3 + n4 == n3n4sum:
                        found = True
                        break
            elif False:
                # n3 + n4 = s
                # n3 * n4 = p
                # n3 = s - n4
                # (s-n4) * n4 = p
                # n4**2 -s*n4 + p = 0
                # solve quadratic
                # n4 = (s +/- math.sqrt(s*s - 4*p)) / 2
                count = count + 1
                s = n3n4sum
                p = n3n4prod
                rootterm = s*s - 4*p
                if rootterm <= 0:
                    continue
                root = math.sqrt(rootterm)
                if root != int(root):
                    continue
                if (s + root) % 2 != 0:
                    continue
                n4 = (s + root) / 2
                n3 = n3n4sum - n4
                if n3 < n2:
                    continue
                found = True
            elif False:
                for n3 in range (n2, int(n3n4sum/2) + 1):
                    count = count + 1
                    n4 = n3n4sum - n3
                    prod = n1 * n2 * n3 * n4
                    if prod == goal:
                        found = True
                        break
            if found:
                print ('... %.2f: %.2f %.2f %.2f %.2f' % (num/100, n1/100, n2/100, n3/100, n4/100))
                finds = finds + 1
                break
        

    if finds > 0:
        print('          %d find%s after %d tries' % (finds, 's' if finds > 1 else '', count) )

                




            
