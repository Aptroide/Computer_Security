# Lab 5: Trust and Digital Certificates

Objective: Digital certificates are used to define a trust infrastructure within PKI (Public Key Infrastructure). A certificate can hold a key pair while a distributable certificate will only contain the public key. In this lab, we will read-in digital certificates and analyse them.

## Lab demo
[![Lab Demo](https://img.youtube.com/vi/-uNQFv0GTZc/0.jpg)](https://youtu.be/-uNQFv0GTZc)

## Exercise 1: Digital Certificate 

**A.1** 

From: 
**Web link (Digital Certificate):**  
[Digital Certificate](http://asecuritysite.com/encryption/digitalcert)

Open up Certificate 1 and identify the following:  
- **Serial number**: 702958
- **Effective date:** 4/24/2008 8:18:42 PM
- **Name:** Fred Smith
- **Issuer:** Fred Smith
- **What is CN used for:** Common Name (Fred Smith) used to identify the subject or entity associated with the certificate. It is the name that identifies the certificate holder within the Domain Name System (DNS) hierarchy and is often used to verify if the certificate matches the domain being accessed.
- **What is ON used for:** Organization Name (None) refers to the legal name of the entity owning the certificate
- **What is O used for:** Organization (Nowhere) refers to the organization of the entity owning the certificate. It provides additional context regarding the identity of the certificate holder, allowing for better assimilation into corporate or institutional structures.
- **What is L used for:** Locality (Edinburgh) indicates the specific geographic location of the certificate holder, usually the city or town. Along with the state/province (S) and country (C), it helps to identify the legal jurisdiction applicable to the certificate holder.

**A.2** 
Open-up the ZIP file for the certificate (Certificate 3) and view the DER file.  
- **What other information can you gain from the certificate:**
    - The two fingerprints that we have on the certificate
    - Public key info.
    - The signature for the signer.
- **What is the size of the public key:** 256 bits
- **Which hashing method has been used:** SHA1
![googel cer info](/Lab5/exercise1/img/2.png)
- **Is the certificate trusted on your system:** [No]
![googel trusted cer](/Lab5/exercise1/img/1.png)

**A.3** 
Make a connection to the www.live.com Web site:
```bash
openssl s_client -connect www.live.com:443
```
- **Can you identify the certificate chain?** Yes
![cer chain](/Lab5/exercise1/img/3.png)

- **What is the subject on the certificate?** outlook.live.com
- **Who is the issuer on the certificate?** DigiCert Cloud Services CA-1
![cer chain](/Lab5/exercise1/img/4.png)


**A.4** 
Google moved in July 2018 to mark sites as being insecure if they did not have a match between their digital certificate and the site. First open a browser and see if you can access testfire.net (you can try both https and http for the connection). 
- Using http:
![http](/Lab5/exercise1/img/5.png)
- Using https:
![https](/Lab5/exercise1/img/6.png)
- **Run a scan from https://www.ssllabs.com/ on testfire.net. What do you observe from the result?**
- **What is the SSLLabs rating on this site? Is it "A", "B", "C", "D", "E" or "F"?** If trust issues are ignored: B

- **What does a “T” rating identify?** It means that the site name doesn't match with the name on the certificate.
- **Can you locate another "T" rated site?** Yes, `diankpi.com` is a "T" rated site.
![T](/Lab5/exercise1/img/7.png)

**A.5** 
Which the certificates in A.2, for Example 2 to Example 6. Complete the following table:

| Cert | Organisation (Issued to) | Date range when valid | Size of public key | Issuer | Root CA | Hash method | Is it trusted? |
|------|--------------------------|-----------------------|--------------------|--------|---------|-------------|---------------|
|2|Nowhere Ltd|2011-10-29 to 2013-10-28|1024 bits |No One| Nowhere Ltd | SHA1WithRSAEncryption | No |
|3|*.google.com|2023-02-08 to 2023-05-03|256 bits |GTS CA 1C3 | Google Trust Services LLC | SHA256WithRSAEncryption | No |
|4|www.cisco.com|2012-07-10 to 2013-07-1|1024 bits |VeriSign Class 3 Secure Server CA - G3 | VeriSign, Inc. | SHA1WithRSAEncryption | No |
|5|microsoft.com|2023-01-13 to 2024-01-08|2048 bits |Microsoft Azure TLS Issuing CA 05 | Microsoft Corporation | SHA384WithRSAEncryption | No |
|6|oracle.com|2023-02-14 to 2024-02-26|2048 bits |DigiCert TLS RSA SHA256 2020 CA1 | Oracle Corporation | SHA256WithRSAEncryption | No |


**A.6** 

Now download the DER files from:

[Web link (Digital Certificate)](http://asecuritysite.com/der.zip)

Now use openssl to read the certificates:
```bash
openssl x509 -inform der -in [certname] -noout -text
```
![T](/Lab5/exercise1/img/8.png)

## Exercise 2: Creating Certificates

**B.1**  
Create your own certificate from:  
**Web link (Create Certificate):**  
[Create Certificate](http://asecuritysite.com/encryption/createcert)

Add in your own details.
![certificate](/Lab5/exercise2/img/1.png)

- **View the certificate and verify some of the details on the certificate.**

| Cert | Organisation (Issued to) | Date range when valid | Size of public key | Issuer | Root CA | Hash method |
|------|--------------------------|-----------------------|--------------------|--------|---------|-------------|
|1|Yachay|2024-03-23 to 2025-03-23|512 bits |IT CA 08| Yachay Tech | RSA |

- **Can you view the DER file?** No
![certificate](/Lab5/exercise2/img/2.png)

We have a root certificate authority of My Global Corp which is based in Washington US and the administrator is admin@myglobalcorp.com and we are going to issue a certificate to My Little Corp which is based in Glasgow UK and the administrator is admin@mylittlecorp.com.

**B.2**  
Create your RSA key pair with:
```bash
openssl genrsa -out ca.key 2048
```

Next create a self-signed root CA certificate ca.crt for **My Global Corp**:
```bash
openssl req -new -x509 -days 1826 -key ca.key -out ca.crt
```

- **How many years will the certificate be valid for?** 5 years (1826 days)
- **Wich the details have you entered:**
    - Country Name.
    - State or Province Name (full name).
    - Locality Name. 
    - Organization Name. 
    - Organizational Unit Name. 
    - Common Name.   
    - Email Address.
![My global Corp](/Lab5/exercise2/img/3.png)

**B.3**  
From your Home folder, open up ca.crt and view the details of the certificate.
- **Which Key Algorithm has been used:** RSA
- **Which hashing methods have been used:** 
- **When does the certificate expire:** 03/23/29
- **Who is it verified by:** Global Corp Inc.
- **Who has it been issued to:** Global Corp Inc.
![My global Corp](/Lab5/exercise2/img/4.png)
**B.4**  
Create a subordinate CA (**My Little Corp**) which will be used for the signing of the certificate. Generate the key:
```bash
openssl genrsa -out ia.key 2048
```
Request a certificate for the newly created subordinate CA:
```bash
openssl req -new -key ia.key -out ia.csr
```
Create a certificate from the subordinate CA signed by the root CA:
```bash
openssl x509 -req -days 730 -in ia.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out ia.crt
```
![My Little Corp](/Lab5/exercise2/img/5.png)
![My Little Corp](/Lab5/exercise2/img/6.png)

- **View the newly created certificate.**
- **When does it expire:** 03/23/26
- **Who is the subject of the certificate:** My Little Corp
- **Which is their country:** EC
- **Who signed the certificate:** Global Corp Inc. (My Global Corp)
- **Which is their country:** EC
- **What is the serial number of the certificate?** 01
- **Check the serial number for the root certificate. What is its serial number?** 3F 30 32 43 18 E9 6A 88 76 93 C6 94 10 4E C0 DE 61 40 46 6F

**B.5**  
Convert the certificate to a PKCS12 file to digitally sign files and verify signatures:
```bash
openssl pkcs12 -export -out ia.p12 -inkey ia.key -in ia.crt -chain -CAfile ca.crt
```
- **Can you view ia.p12 in a text editor?** Yes, but its unreadable.
![My Little Corp](/Lab5/exercise2/img/7.png)

**B.6**  
The crt format is encoded in binary. To export to a Base64 format, we can use DER:
```bash
openssl x509 -inform pem -outform pem -in ca.crt -out ca.cer
```
And for My Little Corp:
```bash
openssl x509 -inform pem -outform pem -in ia.crt -out ia.cer
```

- **View each of the output files in a text editor (ca.cer and then ia.cer). What can you observe from the format:** files are readable, we can inspect the certificate's content in the files using a text editor. 
- **Which are the standard headers and footers used?**
    - **Headers:** -----BEGIN CERTIFICATE-----
    - **Footers:** -----END CERTIFICATE-----

![ca cer](/Lab5/exercise2/img/8.png)
![ia cer](/Lab5/exercise2/img/9.png)

**B.7**  
Run the following program to verify its operation:
```python
import OpenSSL.crypto
from OpenSSL.crypto import load_certificate_request, FILETYPE_PEM

csr = '''
-----BEGIN NEW CERTIFICATE REQUEST-----
... [Your CSR content here] ...
-----END NEW CERTIFICATE REQUEST-----
'''

req = load_certificate_request(FILETYPE_PEM, csr)
key = req.get_pubkey()
key_type = 'RSA' if key.type() == OpenSSL.crypto.TYPE_RSA else 'DSA'
subject = req.get_subject()
components = dict(subject.get_components())
print("Key algorithm:", key_type)
print("Key size:", key.bits())
print("Common name:", components.get('CN', ''))
print("Organisation:", components.get('O', ''))
print("Organisational unit:", components.get('OU', ''))
print("City/locality:", components.get('L', ''))
print("State/province:", components.get('ST', ''))
print("Country:", components.get('C', ''))
```
- `exercise2/b_07.py` is a Python script that loads a certificate request (CSR) in PEM format, extracts information from it, and prints out details about the CSR.

![cer info python](/Lab5/exercise2/img/10.png)

**Web link (CSR):**  
[CSR](https://asecuritysite.com/encryption/csr)

**B.8** 
Checking the signing on these certificate requests:

-----BEGIN NEW CERTIFICATE REQUEST-----

MIICyTCCAbECAQAwajELMAkGA1UEBhMCVUsxDTALBgNVBAgTBE5vbmUxEjAQBgNV
BAcTCUVkaW5idXJnaDEXMBUGA1UEChMOTXkgTGl0dGxlIENvcnAxDDAKBgNVBAsT
A01MQzERMA8GA1UEAxMITUxDLm5vbmUwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAw
ggEKAoIBAQCuQE68qgssJ210wGxfKjCX3PG/RgSb5VpAp2rzavx71M9Bhg9kUORE
OP7BQC3E6DGu+xba3NdnhrHAFNa+hH9dnTZrlxb98aM5q9+TUm76V1toIseOMDdU
UE9IpxXoFvD6b0inbFZnbrjFj3XUUzIIqvvizw4rIOxzgbWqZ5+F7YpP8d59eWW0
6iXzJKoeE/+Gw7Slsdr1+QQAUaX05MHTweMYbZEHir2M8f1RA4o81zEd2tWCK85F
6VS/EkCzUG1cqDBQQ7D2S9MWN8Zk2P7CS8/yZx7uRTmT1t3UWKLUyIN0TU3IjCeY
t53P6C+9DT6UD0fDFZRBCmPOH+qb6/YBAgMBAAGgGjAYBgkqhkiG9w0BCQcxCxMJ
UXdlcnR5MTIzMA0GCSqGSIb3DQEBBQUAA4IBAQCqpXjmaQf2/o/xbNZG5ggAV8yV
d6rSabnov5zIkcit9NQXsPJEi84u7CbcriYqY5h7XlMWjv476mAGbgAVZB2ZhIlp
qLal+lx9xwhFbuLHNRxZcUMM0g9KQZaZTkAQdlDVU/vPzRjq+EHGoPfG7R9QKGD0
k1b4DqOvInWLOs+yuWT7YYtWdr2TNKPpcBqbzCYzrWL6UaUN7LYFpNn4BbqXRgVw
iMAnUh9fvLMe7oreYfTaevXT/506Sj9WvQFXTcLtRhs+M30q22/wUK0ZZ8APjpwf
rQMegvzXXEIO3xEGrBi5/wXJxsawRLcM3ZSGPu/Ws950oM5Ahn8K8HBdKubQ

-----END NEW CERTIFICATE REQUEST-----

- Key algorithm: RSA
- Key size: 2048
- Common name:
- Organisation:
- Organisation unit:
- City/locality:
- State/province
- Country:


-----BEGIN NEW CERTIFICATE REQUEST-----

MIIDPzCCAqgCAQAwZDELMAkGA1UEBhMCQ04xCzAJBgNVBAgTAmJqMQswCQYDVQQH
EwJiajERMA8GA1UEChMIbXhjei5uZXQxETAPBgNVBAsTCG14Y3oubmV0MRUwEwYD
VQQDEwx3d3cubXhjei5uZXQwgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAMQ7
an4v6pHRusBA0prMWXMWJCXY1AO1H0X8pvZj96T5GWg++JPCQE9guPgGwlD02U0B
NDoEABeD1fwyKZ+JV5UFiOeSjO5sWrzIupdMI7hf34UaPNxHo6r4bLYEykw/Rnmb
GKnNcD4QlPkypE+mLR4p0bnHZhe3lOlNtgd6NpXbAgMBAAGgggGZMBoGCisGAQQB
gjcNAgMxDBYKNS4yLjM3OTAuMjB7BgorBgEEAYI3AgEOMW0wazAOBgNVHQ8BAf8E
BAMCBPAwRAYJKoZIhvcNAQkPBDcwNTAOBggqhkiG9w0DAgICAIAwDgYIKoZIhvcN
AwQCAgCAMAcGBSsOAwIHMAoGCCqGSIb3DQMHMBMGA1UdJQQMMAoGCCsGAQUFBwMB
MIH9BgorBgEEAYI3DQICMYHuMIHrAgEBHloATQBpAGMAcgBvAHMAbwBmAHQAIABS
AFMAQQAgAFMAQwBoAGEAbgBuAGUAbAAgAEMAcgB5AHAAdABvAGcAcgBhAHAAaABp
AGMAIABQAHIAbwB2AGkAZABlAHIDgYkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAADANBgkqhkiG9w0BAQUFAAOBgQBIKHVhHb9FZdVLV4VZ
9DK4aBSuYY//jlIpvsfMIdHXfAsuan7w7PH87asp1wdb6lD9snvLZix1UGK7VQg6
wUFYNlMqJh1m7ITVvzhjdnx7EzCKkBXSxEom4mwbvSNvzqOKAWsDE0gvHQ9aCSby
NFBQQMoW94LqrG/kuIQtjwVdZA==

-----END NEW CERTIFICATE REQUEST-----

- Key algorithm: RSA
- Key size: 1024
- Common name:
- Organisation:
- Organisation unit:
- City/locality:
- State/province
- Country:

-----BEGIN CERTIFICATE REQUEST-----

MIIByjCCATMCAQAwgYkxCzAJBgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlh
MRYwFAYDVQQHEw1Nb3VudGFpbiBWaWV3MRMwEQYDVQQKEwpHb29nbGUgSW5jMR8w
HQYDVQQLExZJbmZvcm1hdGlvbiBUZWNobm9sb2d5MRcwFQYDVQQDEw53d3cuZ29v
Z2xlLmNvbTCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEApZtYJCHJ4VpVXHfV
IlstQTlO4qC03hjX+ZkPyvdYd1Q4+qbAeTwXmCUKYHThVRd5aXSqlPzyIBwieMZr
WFlRQddZ1IzXAlVRDWwAo60KecqeAXnnUK+5fXoTI/UgWshre8tJ+x/TMHaQKR/J
cIWPhqaQhsJuzZbvAdGA80BLxdMCAwEAAaAAMA0GCSqGSIb3DQEBBQUAA4GBAIhl
4PvFq+e7ipARgI5ZM+GZx6mpCz44DTo0JkwfRDf+BtrsaC0q68eTf2XhYOsq4fkH
Q0uA0aVog3f5iJxCa3Hp5gxbJQ6zV6kJ0TEsuaaOhEko9sdpCoPOnRBm2i/XRD2D
6iNh8f8z0ShGsFqjDgFHyF3o+lUyj+UC6H1QW7bn

-----END CERTIFICATE REQUEST-----

- Key algorithm: RSA
- Key size: 1024
- Common name:
- Organisation:
- Organisation unit:
- City/locality:
- State/province
- Country:

## Exercise 3: Elliptic Curve Key Creation

**In Openssl we can view the curves with the ecparam option:**
```bash
openssl ecparam -list_curves
```
**Some of the curve names:**
- secp112r2 : SECG curve over a 112 bit prime field
- secp128r2 : SECG curve over a 128 bit prime field
- secp384r1 : NIST/SECG curve over a 384 bit prime field
- prime239v1: X9.62 curve over a 239 bit prime field
- sect163k1 : NIST/SECG/WTLS curve over a 163 bit binary field
- c2pnb163v1: X9.62 curve over a 163 bit binary field
- wap-wsg-idm-ecid-wtls7: SECG/WTLS curve over a 160 bit prime field
- brainpoolP224t1: RFC 5639 curve over a 224 bit prime field
- SM2       : SM2 curve over a 256 bit prime field


**By performing an Internet search, which are the most popular curves (and where are they used)?**

- **NIST P-256 Curve (secp256r1):** Widely used in computer security applications such as TLS/SSL for web communication encryption, email cryptography, and in digital signature systems like ECDSA (Elliptic Curve Digital Signature Algorithm).
- **NIST P-384 Curve (secp384r1):** Mainly used when a higher level of security than P-256 is required, such as in financial and governmental systems, as well as in digital signature and authentication applications.
- **NIST P-521 Curve (secp521r1):** Employed in applications requiring a high level of security, such as in cryptographic key protection and high-level security implementations.
- **Curve25519 and Curve448:** Designed to provide high levels of security and efficiency in applications like key exchange in modern cryptographic protocols such as Signal and WhatsApp, as well as in building disk encryption systems and VPNs.

**We can create our elliptic parameter file with:**

```bash
openssl ecparam -name secp256k1 -out secp256k1.pem
```

Now view the details with:

```bash
openssl ecparam -in secp256k1.pem -text -param_enc explicit -noout
```

![ecc](/Lab5/exercise3/img/1.png)

**What are the details of the key?**
- **Field Type:** Prime field.
- **Prime:** The prime number defining the field, represented in hexadecimal.
- **Coefficient A:** The coefficient A of the elliptic curve equation.
- **Coefficient B:** The coefficient B of the elliptic curve equation.
- **Generator (uncompressed):** The (x, y) coordinates of the base point of the elliptic curve, represented in uncompressed form.
- **Order:** The order of the subgroup generated by the base point, represented in hexadecimal.
- **Cofactor:** The cofactor of the subgroup generated by the base point.

**Now we can create our key pair:**
```bash
openssl ecparam -in secp256k1.pem -genkey -noout -out mykey.pem
```
![ecc](/Lab5/exercise3/img/2.png)

**Now we will encrypt your key pair (and add a password), and convert it into a format which is ready to be converted into a digital certificate:**
```bash
openssl ec -aes-128-cbc -in mykey.pem -out enckey.pem
```
![ecc](/Lab5/exercise3/img/3.png)

**Finally we will convert into a DER format, so that we can import the keys into a system:**
```bash
openssl ec -in enckey.pem -outform DER -out enckey.der
```
![ecc](/Lab5/exercise3/img/4.png)


## Exercise 4: Key Establishment

## Key Management in a Peer-to-Peer Network

In a peer-to-peer network where 1000 users want to communicate in an authenticated and confidential way without a central Trusted Third Party (TTP), we explore key management with symmetric and asymmetric algorithms.

### Symmetric Key Algorithms

1. **How many keys are collectively needed if symmetric algorithms are deployed?**  
   Each pair of users requires a unique key to communicate securely. Therefore, the total number of keys `K` needed can be calculated with the formula `K = n(n-1)/2`, where `n` is the number of users. For 1000 users, this would be `K = 1 000(1 000-1)/2 = 499 500.`

2. **How are these numbers changed if we bring in a central instance (Key Distribution Center, KDC)?**  
   Introducing a KDC means each user needs only one key to communicate with the KDC. Consequently, the total number of keys required reduces to 1000.

3. **What is the main advantage of a KDC against the scenario without a KDC?**  
   The main advantage of a KDC is the drastic reduction in the number of keys required, which simplifies management and improves security. The KDC also centralizes authentication services, allowing for easier monitoring and auditing.

4. **How many keys are necessary if we make use of asymmetric algorithms?**  
   Asymmetric algorithms require two keys per user: a public key and a private key. For 1000 users, this results in 2000 keys in total. Each user must store and manage their private key while their public key is distributed to other users.

Also differentiate between keys which every user has to store and keys which are  collectively necessary.

   - **Keys each user must store:** One private key and 999 public keys of the other users if they wish to communicate with every other user in the network.
   - **Collectively necessary keys:** 1000 private keys and 1000 public keys are necessary for the entire network.

