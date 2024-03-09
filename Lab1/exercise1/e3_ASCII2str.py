import base64

# Define the encoded strings to be decoded
encoded_strings = {
    "Hex": "45637561646F72",
    "Binary": "01011001 01000001 01000011 01001000 01000001 01011001 01010100 01000101 01000011 01001000",
    "Base64_1": "U2VndXJpZGFkIEluZm9ybT90aWNh",
    "Base64_2": "RXNjdWVsYSBkZSBjaWVuY2lhcyBNYXRlbT90aWNhcyB5IENvbXB1dGFjaW9uYWxlcw=="
}

# Function to decode Hexadecimal to ASCII
def decode_hex(s):
    return bytes.fromhex(s).decode()

# Function to decode Binary to ASCII
def decode_binary(s):
    return ''.join([chr(int(binary, 2)) for binary in s.split(' ')])

# Function to decode Base64 to ASCII
def decode_base64(s):
    return base64.b64decode(s).decode('utf-8')

# Dictionary to hold the decoding results
decoding_results = {
    "Hex": decode_hex(encoded_strings["Hex"]),
    "Binary": decode_binary(encoded_strings["Binary"]),
    "Base64_1": decode_base64(encoded_strings["Base64_1"]),
    "Base64_2": decode_base64(encoded_strings["Base64_2"])
}

# Print the decoding results
print(decoding_results)
