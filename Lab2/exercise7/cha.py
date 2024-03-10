from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

def chacha20_encrypt(key, nonce, plaintext):
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return ciphertext

def chacha20_decrypt(key, nonce, ciphertext):
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext

if __name__ == "__main__":
    key = os.urandom(32)  # Generate a 256-bit (32-byte) key
    nonce = os.urandom(12)  # Generate a 96-bit (12-byte) nonce
    nonce = nonce + b'\x00' * (16 - len(nonce))  # Pad nonce to make it 128 bits
    plaintext = b"si se pudo burro"  # Plain text to be encrypted

    ciphertext = chacha20_encrypt(key, nonce, plaintext)
    print("Ciphertext:", ciphertext.hex())

    decrypted_plaintext = chacha20_decrypt(key, nonce, ciphertext)
    print("Decrypted plaintext:", decrypted_plaintext.decode())
