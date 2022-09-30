""" Implement PKCS#7 padding """

# block cipher transforms a fixed-sized block (usually 8 or 16 bytes) of plaintext into ciphertext.
# But we almost never want to transform a single block; we encrypt irregularly-sized messages.
# One way we account for irregularly-sized messages is by padding,
# creating a plaintext that is an even multiple of the block size. The most popular padding scheme is called PKCS#7.
# So: pad any block to a specific block length, by appending the number of bytes of padding to the end of the block.


def pkcs7_padding(message, blocksize):
    pad_length = blocksize - (len(message) % blocksize)

    if pad_length == 0:
        pad_length = blocksize

    padding = bytes([pad_length]) * pad_length

    return message + padding


def pkcs7_strip(data):
    padding_length = data[-1]
    return data[: -padding_length]


yelsub = pkcs7_padding(b'YELLOW SUBMARINE', 20)
print(yelsub)
