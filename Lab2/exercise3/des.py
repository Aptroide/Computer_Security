from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from secrets import token_bytes
import binascii

# Generate a random DES key
key = token_bytes(8)

def encrypt(msg, mode):
    # Create a DES cipher object with the specified padding scheme
    cipher = DES.new(key, DES.MODE_CBC)

    # Get the initialization vector (IV) generated by the cipher
    iv = cipher.iv

    # Pad the message according to the specified padding scheme and then encrypt it
    if mode == "PKCS7":
        padded_msg = pad(msg.encode('ascii'), DES.block_size, style='pkcs7')
    elif mode == "ISO7816":
        padded_msg = pad(msg.encode('ascii'), DES.block_size, style='iso7816')
    elif mode == "x923":
        padded_msg = pad(msg.encode('ascii'), DES.block_size, style='x923')
    else:
        raise ValueError("Unknown padding style")

    ciphertext = cipher.encrypt(padded_msg)

    return iv, ciphertext

# Main function
if __name__ == "__main__":
    # Ask the user to enter a message
    msg = input('Enter a message: ')

    # Iterate over all available padding schemes
    for mode in ["PKCS7", "ISO7816", "x923"]:
        print(f"\nPadding mode: {mode}")

        # Encrypt the message
        iv, ciphertext = encrypt(msg, mode)

        # Convert the ciphertext and the IV to hexadecimal
        ciphertext_hex = binascii.hexlify(ciphertext).decode('ascii')
        iv_hex = binascii.hexlify(iv).decode('ascii')

        # Display the ciphertext and the initialization vector in hexadecimal
        print(f'Cipher text (hex): {ciphertext_hex}')
        print(f'IV (hex): {iv_hex}')