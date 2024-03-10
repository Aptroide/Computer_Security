from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes 
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import hashlib
import binascii

def decrypt(ciphertext, key, mode):
    method = algorithms.AES(key)
    cipher = Cipher(method, mode, default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext

def unpad(data):
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(data) + unpadder.finalize()
    return unpadded_data

if __name__ == "__main__":
    ciphertext_hex = input("Enter ciphertext (in hexadecimal): ")
    ciphertext = binascii.unhexlify(ciphertext_hex)  # Convert the ciphertext from hexadecimal to bytes
    password = input("Enter password: ")
    key = hashlib.sha256(password.encode()).digest()  # Derive a 256-bit key from the password

    plaintext = decrypt(ciphertext, key, modes.ECB())  # Decrypt the ciphertext

    plaintext = unpad(plaintext)  # Remove the PKCS#7 padding

    print("Decrypted plaintext:", plaintext.decode())  # Print the decrypted plaintext
