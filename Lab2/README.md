# Lab 2 - Symmetric Key Encryption

This lab focuses on the principles and practice of symmetric key encryption, utilizing tools such as OpenSSL for encryption tasks.

## Exercise 1 - OpenSSL Fundamentals

In this exercise, we explore the OpenSSL command-line interface and perform operations related to symmetric key encryption.

### 1. Encryption Methods Supported by OpenSSL
Five encryption methods supported by OpenSSL include AES, 3DES, Blowfish, RC4, and ChaCha20.

`![Encryption Methods](/Labs/Lab2/exercise1/1_1.png)`

### 2. Version of OpenSSL
The version of OpenSSL being used for these exercises.

`![OpenSSL Version](/Labs/Lab2/exercise1/1_2.png)`

### 3. Help of OpenSSL
The help menu of OpenSSL provides a comprehensive list of commands and options available.

`![OpenSSL Help](/Labs/Lab2/exercise1/1_3.png)`

### 4. Checking Prime Numbers with OpenSSL
We use the OpenSSL command to check if certain large numbers are prime.
  
`![Prime Check](/Labs/Lab2/exercise1/1_4.png)`

### 5. Generate a random prime number of 4096 bits with OpenSSL
We use the OpenSSL command to generate a random prime number of 4096 bits.
  
`![Prime Check](/Labs/Lab2/exercise1/1_5.png)`

### 6. Encrypt file with aes256.
We use the OpenSSL command to encrypt a file with aes256 encryption.
  
`![Prime Check](/Labs/Lab2/exercise1/1_6.png)`

### 7. Encrypt file with aes256 and -base64 encoding.
We use the OpenSSL command to encrypt a file with aes256 encryption and base64 encoding.
  
`![Prime Check](/Labs/Lab2/exercise1/1_7.png)`

### 8. Encrypt file with aes256, base64 encoding and PBKDF2.
We use the OpenSSL command to encrypt a file with aes256 encryption, base64 encoding and PBKDF2.
  
`![Prime Check](/Labs/Lab2/exercise1/1_8.png)`

Yes, the output has changed because PBKDF2 (Password-Based Key Derivation Function 2) derive the encryption key from the passphrase, which strengthens the security of the passphrase by protecting against brute force and dictionary attacks.

### 9. Decrypt the encrypted file with the correct format.
We use the OpenSSL command to decrypt the previus encrypted file.

#### Using the correct password

`![Prime Check](/Labs/Lab2/exercise1/1_9_1.png)`

#### Using the wrong password

`![Prime Check](/Labs/Lab2/exercise1/1_9_2.png)`

### 10. Encryption with Blowfish.
We use the OpenSSL command to encrypt and decrypt a file using Blowfish.

#### Encrypt command: 
openssl enc -blowfish -in myfile.txt -out encrypted.bin

#### Decrypt command
openssl enc -d -blowfish -in encrypted.bin

#### Using the correct password I decrypt the file

`![Prime Check](/Labs/Lab2/exercise1/1_10.png)`

### 11. Encryption with 3DES.
We use the OpenSSL command to encrypt and decrypt a file using 3DES.

#### Encrypt command: 
openssl enc -des-ede3 -in myfile.txt -out encrypted.bin

#### Decrypt command: 
openssl enc -d -des-ede3 -in encrypted.bin

#### Using the correct password I decrypt the file

`![Prime Check](/Labs/Lab2/exercise1/1_11.png)`

### 12. Encryption with RC2.
We use the OpenSSL command to encrypt and decrypt a file using RC2.

#### Encrypt command: 
openssl enc -rc2 -in myfile.txt -out encrypted.bin


#### Decrypt command: 
openssl enc -d -rc2 -in encrypted.bin


#### Using the correct password I decrypt the file

`![Prime Check](/Labs/Lab2/exercise1/1_12.png)`

## Exercise 2 - Padding (AES)

### 1. Installation of Cryptographic Libraries
Cryptographic libraries have been installed to support AES-256 encryption.

### 2. AES Block Size and Hex Characters
- Block size (bytes): the block size for AES is always 16 bytes, regardless of the key size. The key size (256 bits) just determines the number of rounds in the encryption process.

- Number of hex characters for block size: The block size for AES is 16 bytes. When represented in hexadecimal, each byte is represented by two hex characters. Therefore, the block size for AES is represented by 32 hex characters. We see a proof on `e1.py`.

### 3. Implementation of AES-256 Encryption with Different Padding Schemes
- `e3.py`: Python script to encrypt data using AES-256 with various padding schemes.


### 4. Encryption and Decryption Tests
- `e4.py`: Python script to encryption and decryption tests have been performed using sample data with the following padding schemes:

- PKCS#7 Padding
- ANSI X.923 Padding
- ISO/IEC 7816-4 Padding

The output is the original plaintext because the ciphertext was decrypted using the padding scheme used to encrypt it

<!-- TODO ## Exercise 3 - Padding (DES) -->

## Exercise 4 - Python Coding (Encrypting)

- `cipher01.py`: Python script to encryption and decryption using AES and PKCS7.


| Message    | Key        | CMS Cipher AES                            |
|------------|------------|-------------------------------------------|
| hello      | hello123   | 0a7ec77951291795bac6690c9e7f4c0d          |
| Security   | orange     | 2e5b2dc7f30b60fa64afd3a6fd478797          |
| YachayTech | university | 6c7316eed2c54f7ee50d8e7d5ca81d76          |
| Ecuador    | emerald    | 50f58241232c031f8b0cf7d862e58067          |

- `cipher02.py`: Python script to encryption and decryption using DES.

| Message    | Key        | CMS Cipher DES                            |
|------------|------------|-------------------------------------------|
| hello      | hello123   | 86cc1d0855fd6462                          |
| Security   | orange     | 3437d3ce0739f6f71d807e0e9e83ddcb          |
| YachayTech | university | 17fad29a1f1bedd0873e859d94fc781f          |
| Ecuador    | emerald    | e55443561aae3fde                          |

- `cipher02.py`: Python script to encryption and decryption using DES but the entry is the ciphertext and the password.

## Exercise 5 - Python Coding (Decrypting)
- `cipher02.py`: Python script to decryption using AES.

| CMS Cipher (256-bit AES ECB) | Key      | Plain text  
|------------------------------|----------|------------|
| b436bd84d16db330359edebf49725c62 | hello    | germany |
| 4bb2eb68fccd6187ef8738c40de12a6b | ankle    | spain   |
| 029c4dd71cdae632ec33e2be7674cc14 | changeme | england |
| d8f11e13d25771e83898efdbad0e522c | 123456   | scotland|

- `cipher02.py`: Python script to encryption and decryption using DES.

- `cipher03.py`: Python script to encryption and decryption using 256-bit AES ECB and base64.

| CMS Cipher (256-bit AES ECB) | Key      | Plain text  
|------------------------------|----------|------------|
| /vA6BD+ZXu8j6KrTHi1Y+w== | hello    | italy   |
| nitTRpxMhGlaRkuyXWYxtA== | ankle    | sweden  |
| irwjGCAu+mmdNeu6Hq6ciw== | changeme | belgium |
| 5I71KpfT6RdM/xhUJ5IKCQ== | 123456   | mexico  |

## Exercise 6 - Catching exceptions (Decrypting)
- `cipher01.py`: Python script to try decryption '1jDmCTD1IfbXbyyHgAyrdg==' using 256-bit AES ECB and base64.

The password is 'hello'. 

## Exercise 7 - Stream Ciphers