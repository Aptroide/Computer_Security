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

    - MD5 hex chars: 32 hex characters.
    - SHA-1 hex chars: 40 hex characters.
    - SHA-256 hex chars: 64 hex characters.
    - SHA-384 hex chars: 96 hex characters.
    - SHA-512 hex chars: 128 hex characters.

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

    The file 2.txt have been modified.

     ```bash
    md5sum 1.txt
    md5sum 2.txt
    md5sum 3.txt
    md5sum 4.txt
    ```   
    ![MD5 signatures](/Lab4/exercise1/img/1_3.png)

6. **Comparing files contents**

    a) The files has different contents.

    b) We can observe that they have the same signature. This is know as MD5 collision.

    - Using:
    ```bash
    md5sum order.ps
    md5sum letter_of_rec.ps
    ```
    ![Comparing files contents](/Lab4/exercise1/img/1_4.png)
