from e1_lcg import lcg

# Task 4
sequence, pr = lcg(2175143, 3553, 10653, 1000000, 5)

print(f"For: a={pr[0]}, seed={pr[1]}, c={pr[2]}, m={pr[3]}")
print(f"Generated sequence: {sequence}")