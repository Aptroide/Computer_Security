
import binascii
from Crypto.Cipher import ChaCha20

"""
Python script to decryp the ChaCha20 stream cipher with the key 'qwerty' and a nonce of `0x0000000000000000`
"""

cipher_streams = [
    'e81461e995',
    'eb057fe49e34',
    'e8127ee691315e',
    'fb0562f592304385d4'
]

# The nonce is provided as a hexadecimal string, it needs to be converted to bytes
nonce = binascii.unhexlify('0000000000000000')

# Pad the key 'qwerty' with null bytes up to 32 bytes
key = 'qwerty'.encode().ljust(32, b'\0')

def chacha20_decrypt_corrected(key, nonce, ciphertext):
    cipher = ChaCha20.new(key=key, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

# Decryption function that interprets the plaintext as ASCII strings
def decrypt_chacha20_streams(key, nonce, cipher_streams):
    decrypted_texts = []
    for hex_stream in cipher_streams:
        ciphertext = binascii.unhexlify(hex_stream)
        decrypted_text = chacha20_decrypt_corrected(key, nonce, ciphertext)
        decrypted_texts.append(decrypted_text.decode('ascii'))
    return decrypted_texts

# Decrypting the given cipher streams
decrypted_fruits = decrypt_chacha20_streams(key, nonce, cipher_streams)
print(decrypted_fruits)
