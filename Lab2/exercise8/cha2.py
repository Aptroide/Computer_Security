from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import binascii

def chacha20_decrypt(password, nonce, cipher_stream):
    # Derive the key using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # Key length in bytes (256 bits)
        salt=nonce,
        iterations=100000,  # Number of iterations
        backend=default_backend()
    )
    key = kdf.derive(password)

    # Create the Cipher object and decrypt the cipher stream
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(cipher_stream) + decryptor.finalize()

    return plaintext

if __name__ == "__main__":
    # Password (as bytes)
    password = b"qwerty"
    # Nonce (as bytes)
    nonce = b"\x00" * 16  # 128 bits (16 bytes)
    # Cipher stream (as bytes)
    cipher_stream = bytes.fromhex("e81461e995")  # Provided cipher stream

    # Decrypt the cipher stream to get the plaintext
    plaintext = chacha20_decrypt(password, nonce, cipher_stream)

    # Print the plaintext as a byte sequence
    print("Decrypted plaintext:", plaintext)
