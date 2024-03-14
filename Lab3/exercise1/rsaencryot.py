"""
Encryption and decryption using RSA algorithm of:
public key = {n, e} = {143, 7}
private key = {n, d} = {143, 103}
Using:
Encryption - RSA: C = P^e mod n
Decryption - RSA: P = C^d mod n
"""

# RSA encryption
def rsa_encrypt(msg, e, n):
    return pow(msg, e, n)

# RSA decryption
def rsa_decrypt(ciphertext, d, n):
    return pow(ciphertext, d, n)

# Given values
msg = 83
public_key_n = 143
public_key_e = 7
private_key_d = 103

# Encrypt the message
ciphertext = rsa_encrypt(msg, public_key_e, public_key_n)
print(f'Encrypted message (ciphertext): {ciphertext}')

# Decrypt the message
decrypted_msg = rsa_decrypt(ciphertext, private_key_d, public_key_n)
print(f'Decrypted message (plaintext): {decrypted_msg}')
