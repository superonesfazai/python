# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-26 下午4:29
# @File    : hashlib_test.py

import hashlib

m = hashlib.sha256()
m.update(b"Nobody inspects")
m.update(b" the spammish repetition")
print(m.digest())
print(m.digest_size)
print(m.block_size)
print(hashlib.sha224(b"Nobody inspects the spammish repetition").hexdigest())