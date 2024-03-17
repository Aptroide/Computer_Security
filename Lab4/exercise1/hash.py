import hashlib
"""
    This program hashes a text string using MD5, SHA-1, SHA-256, SHA-384, and SHA-512 algorithms.
"""
# Sample text string
text_string = "Yachay Rules!"

# Hashing the text string using various algorithms
hashes = {
    'MD5': hashlib.md5(text_string.encode()).hexdigest(),
    'SHA-1': hashlib.sha1(text_string.encode()).hexdigest(),
    'SHA-256': hashlib.sha256(text_string.encode()).hexdigest(),
    'SHA-384': hashlib.sha384(text_string.encode()).hexdigest(),
    'SHA-512': hashlib.sha512(text_string.encode()).hexdigest(),
}

for clave, valor in sorted(hashes.items()):
    print(f'{clave}: {valor}, {len(valor)} hex characters.')

