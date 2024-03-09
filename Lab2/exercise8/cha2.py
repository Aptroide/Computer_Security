from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import binascii

def chacha20_decrypt(password, nonce, cipher_stream):
    # Derivar la clave utilizando PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # Longitud de la clave en bytes (256 bits)
        salt=nonce,
        iterations=100000,  # Número de iteraciones
        backend=default_backend()
    )
    key = kdf.derive(password)

    # Crear el objeto Cipher y descifrar el flujo de cifrado
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(cipher_stream) + decryptor.finalize()

    return plaintext

if __name__ == "__main__":
    # Contraseña (como bytes)
    password = b"qwerty"
    # Nonce (como bytes)
    nonce = b"\x00" * 16  # 128 bits (16 bytes)
    # Flujo de cifrado (como bytes)
    cipher_stream = bytes.fromhex("e81461e995")  # Flujo de cifrado proporcionado

    # Descifrar el flujo de cifrado para obtener el texto plano
    plaintext = chacha20_decrypt(password, nonce, cipher_stream)

    # Imprimir el texto plano como una secuencia de bytes
    print("Decrypted plaintext:", plaintext)

