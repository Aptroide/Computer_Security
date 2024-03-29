from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad
import binascii

"""
Modify the cipher02.py to decryption a entry ciphertext with his password.
"""

def decrypt(ciphertext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    ciphertext = binascii.unhexlify(ciphertext)
    padded_plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(padded_plaintext, DES.block_size)
    return plaintext.decode()

if __name__ == "__main__":
    ciphertext = input("Enter ciphertext: ")
    password = input("Enter password: ")

    # Adjust key length
    key = password.ljust(8)[:8].encode()

    decrypted_plaintext = decrypt(ciphertext, key)
    print("Decrypted plaintext:", decrypted_plaintext)
