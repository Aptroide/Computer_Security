import binascii

"""
RC4 encryption and decryption
"""

class RC4:
    def __init__(self, key):
        self.state = list(range(256))  # Initialize state array
        self.key = key
        self.init_ksa()  # Key-scheduling algorithm

    def init_ksa(self):
        j = 0
        for i in range(256):
            j = (j + self.state[i] + self.key[i % len(self.key)]) % 256
            self.state[i], self.state[j] = self.state[j], self.state[i]

    def stream_generator(self):
        i = j = 0
        while True:
            i = (i + 1) % 256
            j = (j + self.state[i]) % 256
            self.state[i], self.state[j] = self.state[j], self.state[i]
            K = self.state[(self.state[i] + self.state[j]) % 256]
            yield K

    def encrypt_decrypt(self, data):
        # The same function can be used for encryption and decryption.
        return bytes([_ ^ next(self.stream) for _ in data])

# Function to demonstrate RC4 encryption and decryption
def rc4_encrypt_decrypt():
    key = b'hello'  # RC4 key
    plaintext = b'Last time we used the key "hello" to encrypt and decrypt a message'
    
    # Encrypt
    rc4_cipher_encrypt = RC4(key)
    rc4_cipher_encrypt.stream = rc4_cipher_encrypt.stream_generator()
    ciphertext = rc4_cipher_encrypt.encrypt_decrypt(plaintext)
    
    # Decrypt
    rc4_cipher_decrypt = RC4(key)
    rc4_cipher_decrypt.stream = rc4_cipher_decrypt.stream_generator()
    decrypted = rc4_cipher_decrypt.encrypt_decrypt(ciphertext)
    
    return binascii.hexlify(ciphertext), decrypted

# Run the RC4 encryption and decryption
corrected_rc4_ciphertext, corrected_rc4_decrypted = rc4_encrypt_decrypt()

# print the results
print(f'Encrypted: {corrected_rc4_ciphertext}')
print(f'Decrypted: {corrected_rc4_decrypted}')
