# coding:utf-8

'''
@author = super_fazai
@File    : 经过身份验证的加密.py
@Time    : 2018/4/19 21:37
@connect : superonesfazai@gmail.com
'''

import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

data = b"a secret message"
aad = b"authenticated but unencrypted data"     # 相联系的数据

key = ChaCha20Poly1305.generate_key()
chacha = ChaCha20Poly1305(key)
nonce = os.urandom(12)
ct = chacha.encrypt(nonce, data, aad)
print(chacha.decrypt(nonce, ct, aad))