# coding:utf-8

'''
@author = super_fazai
@File    : demo_1.py
@Time    : 2018/4/19 21:23
@connect : superonesfazai@gmail.com
'''

from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

# 加密
token = f.encrypt(b"A really secret message. Not for prying eyes.")
print(token.decode())

# 解密
_r = f.decrypt(token)
print(_r)