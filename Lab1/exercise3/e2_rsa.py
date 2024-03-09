# Define the function to perform modular exponentiation
def modular_exponentiation(M, e, p):
    return pow(M, e, p)

# Calculate the modular exponentiation for the given values
modular_expo_results = {
    "(101, 7, 293)": modular_exponentiation(101, 7, 293),
    "(4, 11, 79)": modular_exponentiation(4, 11, 79),
    "(5, 5, 53)": modular_exponentiation(5, 5, 53)
}

# Print the results
print(modular_expo_results)

