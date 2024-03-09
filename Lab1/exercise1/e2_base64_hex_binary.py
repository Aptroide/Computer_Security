import base64

# Define the strings to be converted
strings = ["Hola", "HOLA", "HolA"]

# Function to encode a string to Base64
def encode_base64(s):
    return base64.b64encode(s.encode()).decode()

# Function to encode a string to Hexadecimal
def encode_hex(s):
    return s.encode().hex()

# Function to encode a string to Binary
def encode_binary(s):
    return ' '.join(format(ord(c), '08b') for c in s)

# Dictionary to hold the conversion results
conversion_results = {}

# Perform conversions for each string
for s in strings:
    conversion_results[s] = {
        "Base64": encode_base64(s),
        "Hexadecimal": encode_hex(s),
        "Binary": encode_binary(s)
    }
# Print the conversion results
print(conversion_results)
