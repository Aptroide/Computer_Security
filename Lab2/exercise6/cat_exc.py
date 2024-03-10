from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes 
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import hashlib
import base64
import binascii

def encrypt(plaintext, key, mode):
    method = algorithms.AES(key)
    cipher = Cipher(method, mode, default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(plaintext) + encryptor.finalize()
    return ct

"""
Python program which will try various keys for a cipher
text input, and show the decrypted text. 
"""

def decrypt(ciphertext, key, mode):
    method = algorithms.AES(key)
    cipher = Cipher(method, mode, default_backend())
    decryptor = cipher.decryptor()
    pl = decryptor.update(ciphertext) + decryptor.finalize()
    return pl

def pad(data, size=128):
    padder = padding.PKCS7(size).padder()
    padded_data = padder.update(data)
    padded_data += padder.finalize()
    return padded_data

def unpad(data, size=128):
    unpadder = padding.PKCS7(size).unpadder()
    unpadded_data = unpadder.update(data)
    unpadded_data += unpadder.finalize()
    return unpadded_data

if __name__ == "__main__":
    cipher_b64 = '1jDmCTD1IfbXbyyHgAyrdg=='
    password = ['hello','ankle','changeme','123456']

    # Decode the Base-64 encoded cipher string to get the raw ciphertext
    ciphertext = base64.b64decode(cipher_b64)

    for i in password:
        try:
            key = hashlib.sha256(i.encode()).digest()
            # Decrypt the ciphertext
            decrypted_padded_plaintext = decrypt(ciphertext, key, modes.ECB())

            # Unpad the decrypted plaintext
            decrypted_plaintext = unpad(decrypted_padded_plaintext)
            print("Password:", i)
            print("Decrypted plaintext:", decrypted_plaintext.decode(), "\n")
        except:
            print("Invalid password: ", i)
        
  
