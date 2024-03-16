# Exercise 1: RSA Cryptosystem

1. **Generate an RSA key pair** using the command below. This command produces a key pair in PEM format.

    ```bash
    openssl genpkey -algorithm rsa
    ```
    ![RSA Pair](/Lab3/exercise1/1.png)

2. **View the generated key** in a human-readable format by adding the `-text` option to your command:

    ```bash
    openssl genpkey -algorithm rsa -text 
    ```
    ![RSA Pair h-r](/Lab3/exercise1/2_1.png)
    ![RSA Pair h-r](/Lab3/exercise1/2_2.png)

3. **Specify custom key length and public exponent** using the `-pkeyopt` option:

    ```bash
    openssl genpkey -algorithm rsa -pkeyopt rsa_keygen_bits:512 -pkeyopt rsa_keygen_pubexp:17
    ```
    ![RSA Pair length](/Lab3/exercise1/3.png)

4. **Secure the encrypted key with 128-bit AES**

   a) **Generate a key pair:**

    ```bash
    openssl genrsa -out private.pem 1024
    ```

   b) **View the RSA key pair:**

    ```bash
    openssl rsa -in private.pem -text
    ```
    ![RSA Pair gen](/Lab3/exercise1/4_1.png)
    ![RSA Pair gen](/Lab3/exercise1/4_2.png)

   c) **Secure the private key with 128-bit AES encryption:**

    ```bash
    openssl rsa -in private.pem -aes128 -out key3des.pem
    ```

   d) **Export the public key:**

    ```bash
    openssl rsa -in key3des.pem -out public.pem -outform PEM -pubout
    ```

   e) **Encrypt a message using the public key:**

    ```bash
    openssl pkeyutl -encrypt -inkey public.pem -pubin -in myfile.txt -out file.bin
    ```

   f) **Decrypt the encrypted message using the private key:**

    ```bash
    openssl pkeyutl -decrypt -inkey key3des.pem -in file.bin -out decrypted.txt
    ```
    ![RSA Pair gen and aes encrypt](/Lab3/exercise1/4_3.png)

   g) **Output formats:**

    ```bash
    openssl pkeyutl -encrypt -inkey public.pem -pubin -in myfile.txt -out file.bin
    cat file.bin
    ```
    ![RSA Pair gen and aes encrypt](/Lab3/exercise1/4_4.png)

   h) **Output formats:**

    ```bash
    openssl pkeyutl -encrypt -inkey public.pem -pubin -in myfile.txt -out file.bin -hexdump
    cat file.bin
    ```
    ![RSA Pair gen and aes encrypt](/Lab3/exercise1/4_5.png)

5. **Generating an RSA key pair with a key length of 2048 bits**

   a) **Generating the RSA key:**

    ```bash
    openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
    openssl rsa -pubout -in private_key.pem -out public_key.pem
    ```
    ![RSA 2048](/Lab3/exercise1/5_1.png)

   - **Modulus (n) and Public Exponent (e) and Private Exponent (d):**
    ```bash
    openssl rsa -in private_key.pem -text -noout
    ```
    ![RSA n e](/Lab3/exercise1/5_2.png)
    ![RSA d](/Lab3/exercise1/5_3.png)

   b) **Discussing the significance of each component and its role in RSA encryption and decryption**

     - **Modulus (n):** The modulus is a large integer that is the product of two prime numbers used in the key generation process. It's part of both the public and private keys and is fundamental to the RSA algorithm's security. The difficulty of factoring the modulus into its prime factors underpins the RSA cryptosystem's security.

     - **Public Exponent (e):** The public exponent is a positive integer that, along with the modulus, constitutes the public key. It's used in the encryption process and in verifying digital signatures. A common choice for e is 65537, as it offers a good balance between security and computational efficiency.

     - **Private Exponent (d):** The private exponent is a critical part of the private key and is used in the decryption process and in creating digital signatures. The private exponent is derived from the public exponent and the modulus' prime factors, ensuring that only the holder of the private key can decrypt messages encrypted with the corresponding public key or create signatures that can be verified by the public key.

     - **Encryption:** The sender encrypts the message using the recipient's public key, consisting of the modulus (n) and the public exponent (e). The encrypted message is computed as ciphertext = message^e mod n.

     - **Decryption:** The recipient decrypts the message using their private key, which includes the modulus (n) and the private exponent (d). The original message is recovered by computing message = ciphertext^d mod n.

6. **Key Length and Security**

   Generate RSA key pairs and encryption/decryption with 1024 bits
   - **Using asecuritysite:** 
   ![RSA asecuritysite 1024](/Lab3/exercise1/6_1.png)
   ![RSA asecuritysite 1024](/Lab3/exercise1/6_2.png)


   - **Using Opensl:** 
    ```bash
    time openssl genpkey -algorithm RSA -out rsa_1024_private.pem -pkeyopt rsa_keygen_bits:1024 -text
    time openssl rsa -pubout -in rsa_1024_private.pem -out rsa_1024_public.pem   
    time openssl pkeyutl -encrypt -inkey rsa_1024_public.pem -pubin -in myfile.txt -out file.bin
    time openssl pkeyutl -decrypt -inkey rsa_1024_private.pem -in file.bin -out decrypted.txt

    ```
    ![RSA openssl 1024](/Lab3/exercise1/6_3.png)
    ![RSA openssl 1024](/Lab3/exercise1/6_4.png)

   Generate RSA key pairs and encryption/decryption with 2048 bits

   - **Using asecuritysite:** 
   ![RSA asecuritysite 2048](/Lab3/exercise1/6_5.png)
   ![RSA asecuritysite 2048](/Lab3/exercise1/6_6.png)
    
   - **Using Opensl:** 
    ```bash
    time openssl genpkey -algorithm RSA -out rsa_2048_private.pem -pkeyopt rsa_keygen_bits:2048 -text
    time openssl rsa -pubout -in rsa_2048_private.pem -out rsa_2048_public.pem   
    time openssl pkeyutl -encrypt -inkey rsa_2048_public.pem -pubin -in myfile.txt -out file.bin
    time openssl pkeyutl -decrypt -inkey rsa_2048_private.pem -in file.bin -out decrypted.txt
    ```
    ![RSA openssl 2048](/Lab3/exercise1/6_7.png)
    ![RSA openssl 2048](/Lab3/exercise1/6_8.png)

   Results:

   | Key Length | Tool               | Action             | Total Time (s) |
   |------------|--------------------|--------------------|----------------|
   | 1024 bits  | OpenSSL            | Key Generation     | 0.06           |
   | 1024 bits  | OpenSSL            | Encryption/Decryption | 0.02        |
   | 2048 bits  | OpenSSL            | Key Generation     | 0.39           |
   | 2048 bits  | OpenSSL            | Encryption/Decryption | 0.02        |
   | 1024 bits  | asecuritysite      | Key Generation     | 0.273          |
   | 1024 bits  | asecuritysite      | Encryption/Decryption | 0.003       |`
   | 2048 bits  | asecuritysite      | Key Generation     | 1.492          |
   | 2048 bits  | asecuritysite      | Encryption/Decryption | 0.022       |
   
   **Tradeoff between security and computational efficiency:** 

    The security provided by a 2048-bit key is significantly greater than that of a 1024-bit key due to the exponential increase in the difficulty of factoring the RSA modulus. While the times for encryption and decryption do not increase dramatically, the key generation time is noticeably higher, indicating a trade-off where increased security requires more time for setup.

    Despite the longer key generation times, the actual use of longer keys (in encryption and decryption) does not seem to impose a large penalty in operational time, making the use of 2048-bit keys a practical choice for enhanced security without greatly impacting the performance of encryption and decryption tasks.

7. **RSA public-private Encryption/Decryption**

    Knowing that:

    - Encryption - RSA: C = P^e mod n
    - Decryption - RSA: P = C^d mod n
    
    And given:

    - msg = 83

    - public key = {n, e} = {143, 7}
    - private key = {n, d} = {143, 103}

    We solve:

    - Encryption - RSA: C = 83^7 mod 143 = 8
    - Decryption - RSA: P = 8^103 mod 143 = 83

    proof on `exercise1/rsaencryot.py`

8. **RSA Decryption Exercise**

    Given Bob's public key and the ciphertext we cannot perform RSA decryption and know the plaintext message that Bob has been sent.

# Exercise 2: ElGamal Cryptosystem

1. **Generate an RSA key pair** complete process of encryption and decryption of the message m using the ElGamal algorithm
    ![ElGamal Cryptosystem](/Lab3/exercise2/2.png)

2. **Generate an RSA key pair** Python application for ElGamal encryption and decryption on `exercise2/elgamal.py`

# Exercise 3: Diffie-Hellman key exchange

1. **Diffie-Hellman key exchange** complete process of encryption and decryption of the message m using the ElGamal algorithm
    ![ElGamal Cryptosystem](/Lab3/exercise3/1.png)

2. **Diffie-Hellman key exchange** Python application for Diffie-Hellman key exchangeon `exercise3/dh.py`

# Exercise 4: Elliptic Curves over Finite Fields

1. **Elliptic Curve Order and Cofactor:**
   
    To answer a) anf b) we use:
    ```bash
    openssl ecparam -name secp256k1 -param_enc explicit -text
    ```
    **a)** Order of the secp256k1 elliptic curve: 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
   
    **b)** Cofactor of the secp256k1 elliptic curve: 1

    **c)** Cofactor of the Curve25519 elliptic curve: 8

    **d)** Cofactor of the Curve448 elliptic curve: 4

    **e)** Order of the Curve25519 elliptic curve: 2^252 + 0x14DEF9DEA2F79CD65812631A5CF5D3ED

2. **Multiplication of EC Points:**

3. **Point Addition:**
    (5,8) + (12,6) = (15, 13)
    ![Point Addition](Lab3/exercise4/4_1.png)

4. **Point Multiplication:**
    We use `exercise4/da.py` to reach that P3 = (12,6)

# Exercise 5: Choosing an Elliptic Curve for ECC

1. **OpenSSL (ECC)** 

    a) First we need to generate a private key with:
    ```bash
    openssl ecparam -name secp256k1 -genkey -out priv.pem
    ```

    b) We can view the details of the ECC parameters used with
    ```bash
    openssl ecparam -in priv.pem -text -param_enc explicit -noout
    ```
    ![OpenSSL (ECC)](/Lab3/exercise5/5_1.png)

    Values of interest:
    - Prime (last two bytes): A: 0
    - Prime (last two bytes): B: 7 (0x7)
    - Generator (last two bytes): d4:b8 
    - Order (last two bytes): 41:41

    c) Generating a public key based on private key with:
    ```bash
    openssl ec -in priv.pem -text -noout
    openssl ec -in priv.pem -pubout -out public.pem
    ```
    ![OpenSSL (ECC)](/Lab3/exercise5/5_2.png)

    - The private key has 256 bits and 32 bytes
    - The public key has 256 bits and 32 bytes

    This results came from:
    ```bash
    openssl ec -in priv.pem -text -noout 
    openssl ec -pubin -in public.pem -text -noout
    ```
    ![OpenSSL (ECC)](/Lab3/exercise5/5_3.png)

    d) Displaying th list of available elliptic curves (EC) in OpenSSL
    ```bash
    openssl ecparam -list_curves
    ```
    ![OpenSSL (ECC)](/Lab3/exercise5/5_4.png)

    Outline three curves supported:
    - c2pnb304w1: X9.62 curve over a 304 bit binary field
    - c2tnb359v1: X9.62 curve over a 359 bit binary field
    - c2pnb368w1: X9.62 curve over a 368 bit binary field

    e) Lets select two other curves:
    ```bash
    openssl ecparam -name secp128r1 -genkey -out priv.pem
    openssl ecparam -in priv.pem -text -param_enc explicit -noout
    ```
    ![OpenSSL (ECC)](/Lab3/exercise5/5_5.png)

    ```bash
    openssl ecparam -name secp521r1 -genkey -out priv.pem
    openssl ecparam -in priv.pem -text -param_enc explicit -noout
    ```
    ![OpenSSL (ECC)](/Lab3/exercise5/5_6.png)

    - Diferences of secp128k1, secp256k1 and secp512r1.

    | Curve      | Prime Number (p) Size | Base Point (G) Size | 
    |------------|-------------------------|---------------------|
    | secp128k1  | 128 bits                | 256 bits            | 
    | secp256k1  | 256 bits                | 512 bits            | 
    | secp512r1  | 512 bits                | 1024 bits           | 

    - The naming of elliptic curves provides insights into their characteristics, specially gives the size of the prime number used in their definition.

2. **Points of an elliptic curve using the libnum library** 

    a) On `exercise5/ecc.py` we create an elliptic curve with y^2 = x^3 + 7, and with a prime number of 89, then we generate the first five (x,y) points for the finite field elliptic curve. Those are:
    - (1, 39), (1, 50), (3, 37), (3, 52), (4, 31)