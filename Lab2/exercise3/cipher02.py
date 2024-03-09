from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import sys
import binascii

def encrypt(plaintext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    padded_plaintext = pad(plaintext.encode(), DES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    return binascii.hexlify(ciphertext).decode()

def decrypt(ciphertext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    ciphertext = binascii.unhexlify(ciphertext)
    padded_plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(padded_plaintext, DES.block_size)
    return plaintext.decode()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python cipher_des.py <plaintext> <password>")
        sys.exit(1)

    plaintext = sys.argv[1]
    password = sys.argv[2]

    # Ajustar la longitud de la clave
    key = password.ljust(8)[:8].encode()

    print("Before padding:", plaintext)

    ciphertext = encrypt(plaintext, key)
    print("Cipher (ECB):", ciphertext)

    decrypted_plaintext = decrypt(ciphertext, key)
    print("  decrypt:", decrypted_plaintext)
