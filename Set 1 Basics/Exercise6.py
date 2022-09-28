""" Break Repeating-key XOR"""

# THE BEAST
# Here's how:
# Let KEYSIZE be the guessed length of the key; try values from 2 to (say) 40.
# Write a function to compute the edit distance/Hamming distance between two strings.
# For each KEYSIZE, take the first KEYSIZE worth of bytes, and the second KEYSIZE worth of bytes,
#   and find the edit distance between them. Normalize this result by dividing by KEYSIZE.
# The KEYSIZE with the smallest normalized edit distance is probably the key.
#   You could proceed perhaps with the smallest 2-3 KEYSIZE values.
#   Or take 4 KEYSIZE blocks instead of 2 and average the distances.
# Now that you probably know the KEYSIZE: break the ciphertext into blocks of KEYSIZE length.
# Now transpose the blocks: make a block that is the first byte of every block,
#   and a block that is the second byte of every block, and so on.
# Solve each block as if it was single-character XOR. You already have code to do this.
#   For each block, the single-byte XOR key that produces the best looking histogram is
#   the repeating-key XOR key byte for that block. Put them together and you have the key.

from base64 import b64decode
from binascii import hexlify, unhexlify

# def bxor(a,b):
#     desired_length = len(a) if len(a) > len(b) else len(b)
#
#     a1 = a.zfill(desired_length)
#     b2 = b.zfill(desired_length)
#     return bytes([int(a1)^int(b2) for (a1,b2) in zip(a1,b2)])


def bxor(a, b):
    return bytes([x ^ y for (x, y) in zip(a, b)])


def find_hamming(a, b):
    return sum(bin(byte).count('1') for byte in bxor(a, b))


with open("C:/Users/tamsin.DEV/Documents/GitHub/cryptopalsExercises/Exercise Text Files/6.txt") as file:
    text = file.read()

data = b64decode(text)


def find_keysize(ciphertext, keysize):
    last = 0
    diff = 0
    n = 0
    for i in range(0, len(data), keysize):
        chunk = data[i:i+keysize]
        if last:
            diff += find_hamming(chunk, last)/keysize
            n += 1
        last = chunk
    diff /= n
    return diff


keysize = min(range(2,40), key=lambda x: find_keysize(data, x))
print(keysize)
# outputs 29


