"""Implement Repeating Key XOR"""
from binascii import hexlify, unhexlify

# def bxor(a,b):
#     desired_length = len(a) if len(a) > len(b) else len(b)
#
#     a1 = a.zfill(desired_length)
#     b2 = b.zfill(desired_length)
#     return bytes([int(a1)^int(b2) for (a1,b2) in zip(a1,b2)])


def bxor(a,b):
    return bytes([x^y for (x,y) in zip(a, b)])


incoming_text = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key = b'ICE'

keystreamed = key*(len(incoming_text)//len(key)+1)

ciphert = bxor(incoming_text, keystreamed)
print(ciphert)

result = hexlify(ciphert)
print(result)
