from e1_lcg import lcg

sequence, pr = lcg(22, 35, 31, 100, 5)

print(f"For: a={pr[0]}, seed={pr[1]}, c={pr[2]}, m={pr[3]}")
print(f"Generated sequence: {sequence}")