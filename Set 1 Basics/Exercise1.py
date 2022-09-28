"""Convert hex to base64"""

import codecs

string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
b = string.encode("UTF-8")
output = codecs.encode(codecs.decode(b, 'hex'), 'base64').decode()
print(output)