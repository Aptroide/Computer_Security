from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
import binascii

"""
Python implementation of the ChaCha20 stream cipher.
"""

# Correcting the key length for ChaCha20
def generate_valid_chacha20_key():
    # ChaCha20 requires a 32-byte key
    return get_random_bytes(32)

# Encryption and decryption functions for ChaCha20
def chacha20_encrypt(key, nonce, plaintext):
    cipher = ChaCha20.new(key=key, nonce=nonce)
    ciphertext = cipher.encrypt(plaintext)
    return binascii.hexlify(ciphertext)

def chacha20_decrypt(key, nonce, ciphertext):
    cipher = ChaCha20.new(key=key, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

# Generating a valid key and nonce
valid_key = generate_valid_chacha20_key()
nonce = get_random_bytes(12)  # 96-bit nonce for ChaCha20

# Example plaintext
plaintext = b'Yachay Tech University is the best!'

# Encrypt the plaintext
ciphertext = chacha20_encrypt(valid_key, nonce, plaintext)
print(f'Encrypted: {ciphertext}')

# Decrypt the ciphertext
decrypted = chacha20_decrypt(valid_key, nonce, binascii.unhexlify(ciphertext))
print(f'Decrypted: {decrypted}')