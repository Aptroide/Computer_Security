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
    ciphertext = binascii.unhexlify(ciphertext_hex)  # Convertir el texto cifrado de hexadecimal a bytes
    password = input("Enter password: ")
    key = hashlib.sha256(password.encode()).digest()  # Derivar una clave de 256 bits desde la contraseña

    plaintext = decrypt(ciphertext, key, modes.ECB())  # Descifrar el texto cifrado

    plaintext = unpad(plaintext)  # Eliminar el relleno PKCS#7

    print("Decrypted plaintext:", plaintext.decode())  # Imprimir el texto plano descifrado
