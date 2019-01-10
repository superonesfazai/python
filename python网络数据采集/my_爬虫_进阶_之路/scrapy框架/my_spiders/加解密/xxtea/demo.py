# coding:utf-8

'''
@author = super_fazai
@File    : demo.py
@connect : superonesfazai@gmail.com
'''

# xxtea加解密算法
# pip3 install xxtea
# https://pypi.org/project/xxtea/

import os
import xxtea
import binascii

# Key must be a 16-byte string.
key = os.urandom(16)
print('key: {}'.format(key))
s = b"xxtea is good"

enc = xxtea.encrypt(s, key)
dec = xxtea.decrypt(enc, key)
print(s == dec)

hexenc = xxtea.encrypt_hex(s, key)
print(hexenc)
print(s == xxtea.decrypt_hex(hexenc, key))

from base64 import b64decode

key = os.urandom(16)
s = 'QUvZd5mSBl+PxFo8LFfHOdVRBxbdL6CC0JrFtY/DlOHZQuLhrnRzdUvdq4ZHTCWuNTWCm5/K/pQ8jw8FaX7tPW1QR7ik7FqvDrKIPPEg4n7PjQogcabkyA4cBKk='
xxtea.decrypt(s, key=key)