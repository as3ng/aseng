# Challenge

We're given two files which are a PYC file and an encrypted text file containing the flag respectively. The main objective is pretty obvious, we need to figure out
the `.py` source code back and recover the `flag.txt`. This one's pretty easy.

## TL;DR
* Decompile the PYC file using **uncompyle6**
* Analyze the algorithm used
* Recover the `flag.txt` based on the algorithm

## Decompilation

First, we use the uncompyle6 to decompile the PYC file.

```python
from base64 import b64encode, b32encode, b16encode
import sys

def encrypt(filename):
    fd = open(filename, 'rb')
    data = fd.read()
    fd.close()
    enc_data = data
    for _ in range(12):
        enc_data = b16encode(enc_data)
        enc_data = b32encode(enc_data)
        enc_data = b64encode(enc_data)

    fd = open(filename + '.enc', 'wb')
    fd.write(enc_data)
    fd.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python encryptor.py filename')
        exit()
    encrypt(sys.argv[1])
```
The algorithm is pretty simple, it only encodes the flag.txt with base16, base32, and base64 respectively 12 times so in order
to recover the content back, we just have to reuse the reversed algorithm.

```python
from base64 import b64decode, b32decode, b16decode
import sys

def decrypt(filename):
    fd = open(filename, 'rb')
    data = fd.read()
    fd.close()
    enc_data = data
    for _ in range(12):
        enc_data = b64decode(enc_data)
        enc_data = b32decode(enc_data)
        enc_data = b16decode(enc_data)

    fd = open(filename + 'dec', 'wb')
    fd.write(enc_data)
    fd.close()

print(decrypt("flag.txt.enc"))
```

And we got the flag, **TechnoFairCTF{jUst_Bas1c_ncod3_dc0de_maszzehh!}**
