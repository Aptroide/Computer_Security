# Exercise 1: Hashing.

1. **Using Kali Linux, match the given hash signatures with their corresponding words** 

    We use the command below for each word.

    ```bash
    echo -n 'Falkirk' | openssl md5
    ```
    ![Link Hash](/Lab4/exercise1/img/1_1.png)
    ![Link Hash ans](/Lab4/exercise1/img/1_2.png)

2. **Applying the hash algorithms MD5, SHA-1, SHA-256, SHA-384, and SHA-512** 

    `/Lab4/exercise1/hash.py` python script solution.

3. **Number of hex characters** 

    `/Lab4/exercise1/hash.py` python script solution.

    | Hash Type      | hex characters | 
    |----------------|-----------|
    | MD5      | 32  |
    | SHA-1    | 40  |
    | SHA-256  | 64  |
    | SHA-384  | 96  |
    | SHA-512  | 128 |

4. **Determining the plain-text passwords for given hash entries**

   - bill: **napier**, using:
    ```bash
    openssl passwd -apr1 -salt waZS/8Tm napier
    ```

   - mike: **Ankle123**, using:
    ```bash
    openssl passwd -apr1 -salt mKfrJquI Ankle123
     ```

   - fred: **inkwell**, using:
    ```bash
    openssl passwd -apr1 -salt Jbe/hCIb inkwell  
    ```
   - ian: **password**, using:
    ```bash
    openssl passwd -apr1 -salt 0GyPhsLi password
    ```
   - jane: no world for password provided.
    ```bash
    openssl passwd -1 -salt rqOIRBBN <password>
    ```

5. **Identifying valid MD5 signatures**

    The file 2.txt have been modified, we compare de hash using `/Lab4/exercise1/compare.py` and we use the following commands to create the MD5 hash:

     ```bash
    md5sum 1.txt
    md5sum 2.txt
    md5sum 3.txt
    md5sum 4.txt
    ```   
    ![MD5 signatures](/Lab4/exercise1/img/1_3.png)

6. **Comparing files contents**

    a) The files has different contents.

    b) We can observe that they have the same signature (using `/Lab4/exercise1/compare.py`). This is know as MD5 collision.

    - Using:

    ```bash
    md5sum order.ps
    md5sum letter_of_rec.ps
    ```
    ![Comparing files contents](/Lab4/exercise1/img/1_4.png)

# Exercise 2: Hash Cracking (Hashcat).

1. **Running hashcat help**
    ```bash
    hashcat -- help
    ```
    ![hashcat help](/Lab4/exercise2/img/2_1.png)

2. **Attempt to crack provided MD5 hashes using the words from `/Lab4/exercise2/num2/words`**

    ```bash
    hashcat -m 0 hash1 words
    ```

    | Hash      | Password | 
    |-------------------------|-----------|
    | 232DD5D7274E0D662F36C575A3BD634C  | napier   |
    | 5F4DCC3B5AA765D61D8327DEB882CF99  | password  |
    | 6D5875265D1979BDAD1C8A8F383C5FF5  | Ankle123  |
    | 04013F78ACCFEC9B673005FC6F20698D  | inkwell |

    ![hashcat crack](/Lab4/exercise2/img/2_2.png)
    ![hashcat crack](/Lab4/exercise2/img/2_3.png)

3. **Attempt to crack provided MD5 hashes from `/Lab4/exercise2/num3/hashq3`**

    ```bash
    hashcat -m 0 -a 3 hashq3 
    ```

    | Hash      | Password | 
    |-------------------------|-----------|
    | 8893dc16b1b2534bab7b03727145a2bb  | pear   |
    | 1f3870be274f6c49b3e31a0c6728957f  | apple  |
    | 889560d93572d538078ce1578567b91a  | peach  |
    | 72b302bf297a228a75730123efef7c41  | banana |
    | fe01d67a002dfa0f3ac084298142eccd  | orange |

    ![hashcat crack](/Lab4/exercise2/img/2_4.png)
    ![hashcat crack](/Lab4/exercise2/img/2_5.png)
    ![hashcat crack](/Lab4/exercise2/img/2_6.png)

4. **Attempt to crack provided SHA-256 hash (`/Lab4/exercise2/num4/hashq4`) using the words from `/Lab4/exercise2/num4/wordsq4`**

    ```bash
    hashcat -m 1400 hashq4 wordsq4
    ```

    | Hash      | Password | 
    |-------------------------|-----------|
    | 106a5842fc5fce6f663176285ed1516dbb1e3d15c05abab12fdca46d60b539b7  | help  |

    ![hashcat crack](/Lab4/exercise2/img/2_7.png)
    ![hashcat crack](/Lab4/exercise2/img/2_8.png)

5. **Demonstrate the capability of Hashcat when cracking a NTLM hash**

    Sice we know that the password is `help`, we add `?l?l?l?l` to simplify the search.

    ```bash
    hashcat -m 1000 -a 0 0333c27eb4b9401d91fef02a9f74840e ?l?l?l?l
    ```

    | Hash      | Password | 
    |-------------------------|-----------|
    | 0333c27eb4b9401d91fef02a9f74840e  | help  |

    ![hashcat NTLM crack](/Lab4/exercise2/img/2_9.png)
    ![hashcat NTLM crack](/Lab4/exercise2/img/2_10.png)

6. **Attempt to crack Scottish football team**

    We know that we are looking for Scottish football team, so we create a `/Lab4/exercise2/num6/words6` file with all the possible answers using SHA-256 hash (`/Lab4/exercise2/num6/hashq6`) as input.

    ```bash
    hashcat -m 1400 hashq6 words6
    ```

    | Hash      | Password | 
    |-------------------------|-----------|
    | 635450503029fc2484f1d7eb80da8e25bdc1770e1dd14710c592c8929ba37ee9  | celtic |
    | b3cb6d04f9ccbf6dfe08f40c11648360ca421f0c531e69f326a72dc7e80a0912  | falkirk  |
    | bc5fb9abe8d5e72eb49cf00b3dbd173cbf914835281fadd674d5a2b680e47d50  | aberdeen  |
    | 6ac16a68ac94ca8298c9c2329593a4a4130b6fed2472a98424b7b4019ef1d968  | livingston |

    ![hashcat NTLM crack](/Lab4/exercise2/img/2_11.png)
    ![hashcat NTLM crack](/Lab4/exercise2/img/2_12.png)

7. **Attempt to crack SHA-256 using brute force attack**

    Using`/Lab4/exercise2/num7/hashq7` as our SHA-256 hashs.

    ```bash
    hashcat -a 3 -m 1400 hashq7 ?l?l?l?l?l?l?l?l --increment
    ```

    | Hash      | Password | 
    |-------------------------|-----------|
    | 4dc2159bba05da394c3b94c6f54354db1f1f43b321ac4bbdfc2f658237858c70  | hair |
    | 0282d9b79f42c74c1550b20ff2dd16aafc3fe5d8ae9a00b2f66996d0ae882775  | face  |
    | 47c215b5f70eb9c9b4bcb2c027007d6cf38a899f40d1d1da6922e49308b15b69  | eye  |

    ![hashcat NTLM crack](/Lab4/exercise2/img/2_13.png)
    ![hashcat NTLM crack](/Lab4/exercise2/img/2_14.png)
    