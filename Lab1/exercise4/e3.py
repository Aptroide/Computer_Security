from e1_lcg import lcg

# Task 3
sequence, pr = lcg(954365343, 436241, 55119927, 1000000, 5)

print(f"For: a={pr[0]}, seed={pr[1]}, c={pr[2]}, m={pr[3]}")
print(f"Generated sequence: {sequence}")