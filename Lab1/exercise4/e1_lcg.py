def lcg(a, X_0, c, m, n):
    # Linear Congruential Generator function to generate 'n' numbers of the sequence.
    numbers = []
    aux = [a, X_0, c, m]
    for _ in range(1, n):  
        if len(numbers) == 0:        
            x1 = (a * X_0 + c) % m
            numbers.append(x1)
        else:
            numbers.append((a * numbers[-1] + c) % m)
    return numbers, aux

# Task 1
sequence, pr = lcg(21, 35, 31, 100, 6)
# Prove that the sequence is correct
assert sequence == [ 66, 17, 88, 79, 90], f"Sequence mismatch: {sequence}"

print(f"For: a={pr[0]}, seed={pr[1]}, c={pr[2]}, m={pr[3]}")
print(f"Generated sequence: {sequence}")
