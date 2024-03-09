import os

# Generate a random 16-byte block
block = os.urandom(16)

# Convert the block to a hexadecimal string
hex_block = block.hex()

print(hex_block)
print(len(hex_block))