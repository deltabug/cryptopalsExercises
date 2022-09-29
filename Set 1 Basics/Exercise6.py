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
import string
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

def tracker_single_bytexor(ciphertext2):
    best = None
    for i in range(2**8):
        candidate_key = i.to_bytes(1, byteorder='big')
        keystream = candidate_key*len(ciphertext2)
        candidate_message = bxor(ciphertext2,keystream)
        ascii_chars = list(range(97, 122)) + [32]
        nb_letters = sum([x in ascii_chars for x in candidate_message])

        if best == None or nb_letters > best['nb_letters']:
            best = {"message": candidate_message, 'nb_letters': nb_letters, 'key': candidate_key}
    return best


def single_xor(ciphertext, key):
    plain = [x ^ key for x in ciphertext]
    return bytes(plain)


def english_score(data):
    s = 0
    data = data.lower()
    common = b"etaoin shrdlu"[::-1]

    for c in data:
        if chr(c) not in string.printable:
            return 0

        i = common.find(c)
        if i != -1:
            s += i

    return s


key = []
blocks = [data[i:i+keysize] for i in range(0, len(data), keysize)]

for key_i in range(keysize):
    chunk = b""
    for bl in blocks:
        if key_i < len(bl):
            chunk += bytes([bl[key_i]])

    k = max(range(255), key=lambda x: english_score(single_xor(data, x)))
    key.append(k)





# other attempts
def find_keysize(ciphetext):
    norm = None
    keyl = None
    for keysize in range(2, 41):

        start = 0
        end = start + keysize

        alpha_chunk = ciphetext[start:end]
        beta_chunk = ciphetext[start + keysize:end + keysize]

        hamming_dist = find_hamming(alpha_chunk, beta_chunk)
        normalize = hamming_dist / keysize

        if norm is None or normalize < norm:
            norm = normalize
            keyl = keysize

            # keyl = min(norm.keys(), key=(lambda k:norm[k]))

    return keyl


keys = find_keysize(ciphetext)
print(keys)


def chunked(keylength, ciphetext):
    text = ciphetext
    chunked_list = list()
    chunk_size = keylength

    for i in range(0, len(ciphetext), chunk_size):
        chunked_list.append(ciphetext[i:i + chunk_size])

    return chunked_list

keys = find_keysize(ciphetext)
message_chunk = chunked(keys, ciphetext)
print(message_chunk)


def transposingtime(keylength, ciphetext):
    chunks = dict.fromkeys(range(keylength))

    i = 0
    for octet in ciphetext:
    # If we're at the end of the key start at the beginning again. This
    # is "repeating key" XOR after all.
        if (i == keylength): i = 0

    # If the chunk is null, initialize it to an empty array.
        if (chunks[i] == None): chunks[i] = []

    # Append the current octet to the chunk.
        chunks[i].append(octet)

        i += 1

    print(chunks)


tb = transposingtime(keys, message_chunk)


def attackingnow(keysize, ciphetext):
    message_parts = list()

    for i in range(keysize):
        part = attack_single_bytexor(bytes(ciphetext[i::keysize]))
        message_parts.append(part)

    message = bytes()
    for i in range(max(map(len, message_parts))):
        message += bytes([part[i] for part in message_parts if len(part) >= i + 1])

    return message


for (line_nb, ciphertext2) in enumerate(cipherlsit):
    try:
        message = attack_single_bytexor(ciphertext2)['message']
    except Exception:
        pass
    else:
        candidates.append({
            'line_nb': line_nb,
            'ciphertext': ciphertext,
            'message': message
        })

if len(candidates) > 1:
    print("Too many options")
else:
    for (key, value) in candidates[0].items():
        print(f'{key}: {value}')
