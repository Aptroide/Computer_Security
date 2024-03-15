from random import randint

"""
Diffie-Hellman Key Exchange
"""

# Given public parameters
p = 23  # Prime number
g = 5   # Base

# Alice and Bob's private keys
a = 11  # Alice's private key
b = 7  # Bob's private key

# Random private keys
# a = randint(1, p-2)  # Random Alice's private key
# b = randint(1, p-2)  # Random Bob's private key

# Public keys
A = pow(g, a, p)  # Alice's public key
B = pow(g, b, p)  # Bob's public key

# Shared secrets
s_Alice = pow(B, a, p)  # Alice's shared secret
s_Bob = pow(A, b, p)    # Bob's shared secret

# The shared secret should be the same for both Alice and Bob
assert s_Alice == s_Bob

print(f"Alice's shared secret: {s_Alice}")
print(f"Bob's shared secret: {s_Bob}\n")
print(f"Alice's public key: {A}")
print(f"Bob's public key: {B}")
