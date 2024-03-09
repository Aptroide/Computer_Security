# Using c to check if a number is prime
def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True


if __name__ == "__main__":
    # Define the numbers to be checked for primality
    numbers_to_check = [858599509, 982451653, 982451652]

    # Check if the given numbers are prime
    primality_results = {n: is_prime(n) for n in numbers_to_check}

    # Print the results
    for i in primality_results:
        if primality_results[i]:
            print(f'{i} is prime')
        else:
            print(f'{i} is not prime')