# Formula is 2*N**2 = S(S+1)
# N = Alice's #
# S = total on street
# S**2 + S - 2*N**2 = 0
# roots = (-1 +- sqrt(1-4*2*N**2)) / 2

lolim = 1
hilim = 100000

for N in range (lolim, hilim):
    if (N % 10000 == 0):
        print(f'...{N}');
    TNS = 2*N*N
    # print(N)
    for S in range (N+1, hilim):
        SS = S*(S+1)
        if (SS == TNS):
            print (N, S)
        if (SS > TNS):
            break
