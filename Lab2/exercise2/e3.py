from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
""" 
    Encrypts a plaintext using AES in CBC mode with a given key and multiple padding scheme.
"""
def encrypt_with_padding(plaintext, key, padding_scheme):
    cipher = AES.new(key, AES.MODE_CBC)
    if padding_scheme == 'pkcs7':
        padded_text = pad(plaintext, AES.block_size, style='pkcs7')
    elif padding_scheme == 'x923':
        padded_text = pad(plaintext, AES.block_size, style='x923')
    elif padding_scheme == 'iso7816':
        padded_text = pad(plaintext, AES.block_size, style='iso7816')

    return cipher.iv, cipher.encrypt(padded_text)

# Plain text on UTF-8 or ASCII format
plaintext = b'dont do the labs at the end'
key = get_random_bytes(32)  # AES-256 key (32 bytes)

if __name__ == "__main__":
    # Encrypt the plaintext with different padding schemes
    iv_pkcs7, ciphertext_pkcs7 = encrypt_with_padding(plaintext, key, 'pkcs7')
    iv_x923, ciphertext_x923 = encrypt_with_padding(plaintext, key, 'x923')
    iv_iso7816, ciphertext_iso7816 = encrypt_with_padding(plaintext, key, 'iso7816')

    # Print ciphertext for each padding scheme (IV is also printed for reference)
    print(f'IV (pkcs7): {iv_pkcs7.hex()}')
    print(f'Ciphertext (pkcs7): {ciphertext_pkcs7.hex()}')
    print(f'\nIV (x923): {iv_x923.hex()}')
    print(f'Ciphertext (x923): {ciphertext_x923.hex()}')
    print(f'\nIV (iso7816): {iv_iso7816.hex()}')
    print(f'Ciphertext (iso7816): {ciphertext_iso7816.hex()}')
