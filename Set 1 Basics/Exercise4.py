"""Detect single character XOR"""

#  One of the 60-character strings in this file has been encrypted by single-character XOR.
# Find it.

from typing_extensions import ParamSpecArgs
from binascii import hexlify, unhexlify


with open('../Exercise Text Files/4.txt') as datafile:
    cipherlsit = [unhexlify(line.strip()) for line in datafile]

# def bxor(a,b):
#     desired_length = len(a) if len(a) > len(b) else len(b)
#
#     a1 = a.zfill(desired_length)
#     b2 = b.zfill(desired_length)
#     return bytes([int(a1)^int(b2) for (a1,b2) in zip(a1,b2)])


def bxor(a,b):
    return bytes([x^y for (x,y) in zip(a, b)])


def attack_single_bytexor(ciphertext2):
    best = {"nb_letters": 0}
    for i in range(2 ** 8):
        candidate_key = i.to_bytes(1, byteorder='big')
        candidate_message = bxor(ciphertext2, candidate_key * len(ciphertext2))
        ascii_chars = list(range(97, 122)) + [32]
        nb_letters = sum([x in ascii_chars for x in candidate_message])
        if nb_letters > best['nb_letters']:
            best = {"message": candidate_message, 'nb_letters': nb_letters, 'key': candidate_key}

    if best['nb_letters'] > 0.7 * len(ciphertext2):
        return best
    else:
        pass


candidates = list()

for (line_nb, ciphertext2) in enumerate(cipherlsit):
    try:
        message = attack_single_bytexor(ciphertext2)['message']
    except Exception:
        pass
    else:
        candidates.append({
            'line_nb': line_nb,
            'ciphertext': ciphertext2,
            'message': message
        })

if len(candidates) > 1:
    print("Too many options")
else:
    for (key, value) in candidates[0].items():
        print(f'{key}: {value}')
