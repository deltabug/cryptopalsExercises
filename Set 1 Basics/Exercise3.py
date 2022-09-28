""" Single-Byte XOR Cipher """

# Given the stream of bytes text the function computes the fitting
# quotient of the letter frequency distribution for text
# with the letter frequency distribution of the English language.

# The function returns the average of the absolute difference between
# the frequencies (in percentage) of letters in text
# and the corresponding letter in the English Language.

from binascii import hexlify, unhexlify

ciphertext = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
ciphex = bin(int(ciphertext, 16))[2:]

ciphertextuhex = unhexlify(ciphertext)

candidate_key = bytes([1])
keystream = candidate_key*len(ciphertextuhex)


# def bxor(a,b):
#     desired_length = len(a) if len(a) > len(b) else len(b)
#
#     a1 = a.zfill(desired_length)
#     b2 = b.zfill(desired_length)
#     return bytes([int(a1)^int(b2) for (a1,b2) in zip(a1,b2)])

def bxor(a,b):
    return bytes([x^y for (x,y) in zip(a, b)])


def tracker_single_bytexor(ciphertextuhex):
    best = None
    for i in range(2**8):
        candidate_key = i.to_bytes(1, byteorder='big')
        keystream = candidate_key*len(ciphertextuhex)
        candidate_message = bxor(ciphertextuhex,keystream)
        ascii_chars = list(range(97, 122)) + [32]
        nb_letters = sum([x in ascii_chars for x in candidate_message])

        if best == None or nb_letters > best['nb_letters']:
            best = {"message": candidate_message, 'nb_letters': nb_letters, 'key': candidate_key}
    return best


result = tracker_single_bytexor(ciphertextuhex)

print('key:', result['key'])
print('message:', result['message'])
print('Number of letters:', result['nb_letters'])
