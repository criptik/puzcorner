# F = 9*C/5 + 32

# # rotate last digit to first
# # assume 4 digits
# # last digit of C (and first digit of F) is always 5

# C = k * 10 + 5

# for n digits
# F = 5*10^n + k
# 9*(k*10 + 5)/5 + 32 = 5*10^n + k
# (90*k + 45) / 5 + 32 = 5*10^n + k
# 18*k + 9 + 32 = 5*10^n + k
# 17*k = 5*10^n - 41

for n in range(1, 100):
    big = 5 * 10 ** n - 41
    if (big % 17) == 0:
        k = big//17
        C = k*10 + 5
        F = 9*C//5 + 32
        print(n, C, F)
    
