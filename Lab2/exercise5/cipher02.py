from Crypto.Cipher import DES
import binascii

"""
DES ECB decryption
Modify version cipher02.py, so that you can enter the cipher text, and an encryption key, 
and the code will decrypt to provide the result. But it doesnt works :( the pad is always wrong
"""

def decrypt(ciphertext, key):
    cipher = DES.new(key, DES.MODE_CBC)
    ciphertext = binascii.unhexlify(ciphertext)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

if __name__ == "__main__":
    ciphertext = input("Enter ciphertext (in hexadecimal): ")
    password = input("Enter password: ")

    # Adjust key length
    key = password.ljust(8)[:8].encode()

    decrypted_plaintext = decrypt(ciphertext, key)
    print("Decrypted plaintext:", decrypted_plaintext)

    # Attempt to decode the decrypted plaintext as UTF-8 text
    try:
        print("Decrypted plaintext:", decrypted_plaintext.decode('utf-8'))
    except UnicodeDecodeError:
        print("Decrypted data is not valid UTF-8 or is binary/non-textual.")
