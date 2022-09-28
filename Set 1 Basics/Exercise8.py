"""Detect AES in ECB Mode"""

# File contains a bunch of hex-encoded ciphertexts
# one of them is encrypted with ECB. Detect it

from binascii import hexlify, unhexlify

with open('C:/Users/tamsin.DEV/Documents/GitHub/cryptopalsExercises/Exercise Text Files/8.txt') as file:
    ciphers = [unhexlify(line.strip()) for line in file]


def blocks_repeating(cipher, size=16):
    if len(cipher) % size !=0:
        raise Exception('Ciphertext is not a blocksize multiple')
    else:
        numblocks = len(cipher)//size

    blocks = [cipher[i*size:(i+1)*size] for i in range(numblocks)]

    if len(set(blocks)) != numblocks:
        return True
    else:
        return False


hits = [cipher for cipher in ciphers if blocks_repeating(cipher)]

print(hits)
