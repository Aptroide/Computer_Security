# Define a function to calculate the GCD using the Euclidean algorithm
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Define the pairs of numbers for which to calculate the GCD
pairs = [(7001, 10), (4539, 6)]

for a, b in pairs:
    print(f'The GCD of {a} and {b} is {gcd(a, b)}')
