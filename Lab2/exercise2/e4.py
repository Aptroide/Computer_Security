from e3 import encrypt_with_padding
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad

# Plain text on UTF-8 or ASCII format
plaintext = b'dont do the labs at the end'
key = get_random_bytes(32)  # AES-256 key (32 bytes)

# Encrypt and decrypt with 'pkcs7' padding
iv_pkcs7, ciphertext_pkcs7 = encrypt_with_padding(plaintext, key, 'pkcs7')
cipher = AES.new(key, AES.MODE_CBC, iv=iv_pkcs7)
decrypted_text = cipher.decrypt(ciphertext_pkcs7)
original_plaintext = unpad(decrypted_text, AES.block_size, style='pkcs7')
print(f"Encrypted text: {ciphertext_pkcs7.hex()}")
print(f"Original plaintext: {original_plaintext}\n")


# Encrypt and decrypt with 'x923' padding
iv_x923, ciphertext_x923 = encrypt_with_padding(plaintext, key, 'x923')
cipher_x923 = AES.new(key, AES.MODE_CBC, iv=iv_x923)
decrypted_text_x923 = cipher_x923.decrypt(ciphertext_x923)
original_plaintext_x923 = unpad(decrypted_text_x923, AES.block_size, style='x923')
print(f"Encrypted text: {ciphertext_x923.hex()}")
print(f"Original plaintext: {original_plaintext_x923}\n")

# Encrypt and decrypt with 'iso7816' padding
iv_iso7816, ciphertext_iso7816 = encrypt_with_padding(plaintext, key, 'iso7816')
cipher_iso7816 = AES.new(key, AES.MODE_CBC, iv=iv_iso7816)
decrypted_text_iso7816 = cipher_iso7816.decrypt(ciphertext_iso7816)
original_plaintext_iso7816 = unpad(decrypted_text_iso7816, AES.block_size, style='iso7816')
print(f"Encrypted text: {ciphertext_iso7816.hex()}")
print(f"Original plaintext: {original_plaintext_iso7816}")
