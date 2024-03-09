# Function to check if a number is prime
from e4_prime_check import is_prime

# Function to find the highest prime number within a given range
def find_highest_prime(range_limit):
    for num in range(range_limit, 1, -1):
        if is_prime(num):
            return num

# Find the highest primes in the given ranges
ranges = [100, 1000, 5000, 10000]
highest_primes = {range_limit: find_highest_prime(range_limit) for range_limit in ranges}

print("Highest Prime Numbers:")
for range_limit, prime in highest_primes.items():
    print(f"Up to {range_limit}: {prime}")
