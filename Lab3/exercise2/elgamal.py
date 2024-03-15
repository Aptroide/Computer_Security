from sympy import mod_inverse

# Given values from the provided details
p = 23  # Prime number
alpha = 5   # Generator
d = 7   # Private key (d) used during encryption

# key components
beta = pow(alpha, d, p)  # β = α^d mod p
K_pub = (p, alpha, beta)  # Public key tuple (p, α, β)
k_pr = (p, d)  # Private key tuple (p, d)

# Given encryption values
m = 10  # Message that Alice wants to encrypt
i = 12  # Alice's chosen private key 'i' for her ephemeral key pair

# Alice computes her ephemeral key
K_E = pow(alpha, i, p)  # K_E = α^i mod p

# Alice computes the shared secret
K_M = pow(beta, i, p)  # K_M = β^i mod p

# Alice computes the cipher text
y = (m * K_M) % p

# The encrypted message
ciphertext = (K_E, y)

# Bob's decryption process
def elgamal_decrypt(c1, c2, d, p):
    # Bob computes the shared secret from the cipher text
    K_M = pow(c1, d, p)
    
    # Bob calculates the modular inverse of the shared secret
    K_M_inv = mod_inverse(K_M, p)
    
    # Bob recovers the message
    m = (c2 * K_M_inv) % p
    return m

# Decrypt the message using Bob's private key 'd'
decrypted_message = elgamal_decrypt(ciphertext[0], ciphertext[1], d, p)

print(f'Public key: {K_pub}')
print(f'Private key: {k_pr}')

print(f'Ciphertext: {ciphertext}')
print(f'Decrypted message: {decrypted_message}')
