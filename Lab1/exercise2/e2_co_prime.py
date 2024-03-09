# Define a function to calculate the GCD using the Euclidean algorithm
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Define the pairs of numbers to be checked for co-primality
pairs = [(5435, 634), (5432, 634)]

# Calculate the GCD for each pair and determine if they are co-prime
# by checking if the GCD is 1

for a, b in pairs:
    gcd_result = gcd(a, b)
    if gcd_result == 1:
        print(f'{a} and {b} are co-prime')
    else:
        print(f'{a} and {b} are not co-prime')
 
gcd_result
