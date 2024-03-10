from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes 
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import hashlib
import sys
import binascii

"""
Using AES.
Given the plaintext and the password, the code will generate the ciphertext.
"""

def encrypt(plaintext,key, mode):
    method=algorithms.AES(key)
    cipher = Cipher(method,mode, default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(plaintext) + encryptor.finalize()
    return(ct)

def pad(data,size=128):
    padder = padding.PKCS7(size).padder()
    padded_data = padder.update(data)
    padded_data += padder.finalize()
    return(padded_data)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python cipher01.py <plaintext> <password>")
        sys.exit(1)

    plaintext = sys.argv[1]
    password = sys.argv[2]

    key = hashlib.sha256(password.encode()).digest()

    print("Before padding:", plaintext)

    plaintext = pad(plaintext.encode())

    print("After padding (CMS):", binascii.hexlify(bytearray(plaintext)))

    ciphertext = encrypt(plaintext, key, modes.ECB())
    print("Cipher (ECB):", binascii.hexlify(bytearray(ciphertext)))
