# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-26 下午4:29
# @File    : hashlib_test.py

'''
hashlib里面都是哈希(即加密)算法
'''

import hashlib

m = hashlib.sha256()
m.update(b"Nobody inspects")
m.update(b" the spammish repetition")
print(m.digest())
print(m.digest_size)
print(m.block_size)
print(hashlib.sha224(b"Nobody inspects the spammish repetition").hexdigest())

print('--------- 分割线 ----------')

import hashlib

m = hashlib.md5()       # 创建一个hash对象, md5:(message-Digest Algorithm 5)消息摘要算法,得出⼀个128位的密⽂

print(m)                    # <md5 HASH object>
# python3中unicode编码的字符串在进行哈希运算时必须先转换成字节码编码, 即得传入一个字节码
m.update('super_fazai'.encode())     # 更新哈希对象以字符串参数
print(m.hexdigest())        # 返回十六进制数字字符串

print('--------- 分割线 ----------')

# 实用案例
# 用于注册, 登陆...
import hashlib
import datetime

KEY_VALUE = 'afa'
now = datetime.datetime.now()
m = hashlib.md5()

str = '%s%s' % (KEY_VALUE, now.strftime("%Y%m%d"))
m.update(str.encode())
value = m.hexdigest()
print(value)


'''
python3下测试结果:
b'\x03\x1e\xdd}Ae\x15\x93\xc5\xfe\\\x00o\xa5u+7\xfd\xdf\xf7\xbcN\x84:\xa6\xaf\x0c\x95\x0fK\x94\x06'
32
64
a4337bc45a8fc544c03f52dc550cd6e1e87021bc896588bd79e901e2
--------- 分割线 ----------
<md5 HASH object @ 0x1069695f8>
1275468b27227eea8adaadef828fcd6c
--------- 分割线 ----------
284e933752054a4643e3d2fe8b0157aa
'''