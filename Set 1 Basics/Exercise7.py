""" AES in ECB Mode"""
# The Base64-encoded content in this file has been encrypted via AES-128 in ECB mode under the key
# "YELLOW SUBMARINE".
# (case-sensitive, without the quotes; exactly 16 characters; I like "YELLOW SUBMARINE"
# because it's exactly 16 bytes long, and now you do too).
# Decrypt it. You know the key, after all.
# Easiest way: use OpenSSL::Cipher and give it AES-128-ECB as the cipher.

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64decode

backend = default_backend()


def decrypt_aes(cytext, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(cytext) + decryptor.finalize()

    outmessage = decrypted
    return outmessage


with open("Exercise Text Files/7.txt") as file:
    data = file.read()

print(decrypt_aes(cytext=b64decode(data),
                  key=b'YELLOW SUBMARINE').decode())
