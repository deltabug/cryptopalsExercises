"""Fixed XOR """

# turning string into integer
xorstring = bin(int('1c0111001f010100061a024b53535009181c', 16))[2:]
key = bin(int('686974207468652062756c6c277320657965', 16))[2:]

# make the two the same length
desired_length = len(xorstring) if len(xorstring) > len(key) else len(key)

b1 = xorstring.zfill(desired_length)
b2 = key.zfill(desired_length)

# XOR the 2 and change the result from a list to a string before then going from binary to hex
result = [int(b1)^int(b2) for b1,b2 in zip(b1,b2)]

stresult = "".join([str(bits) for bits in result])

final = hex(int(stresult, 2))[2:0]

print(final)