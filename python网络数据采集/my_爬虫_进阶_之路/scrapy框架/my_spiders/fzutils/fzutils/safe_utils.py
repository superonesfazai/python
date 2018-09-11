# coding:utf-8

"""
安全相关
"""

from uuid import uuid1, uuid3
from uuid import NAMESPACE_DNS
from hashlib import md5

__all__ = [
    'encrypt',              # 加密算法
    'decrypt',              # 解密算法
    'md5_encrypt',          # 得到md5加密的字符串
    'get_uuid1',            # 根据时间戳等, 随机生成一个唯一的uuid
    'get_uuid3',            # 得到一个uuid3加密的唯一标识符
]

def encrypt(key, tmp_str):
    '''
    加密算法
    :param key: 配合加密的key
    :param tmp_str: 待加密的str
    :return:
    '''
    b = bytearray(str(tmp_str).encode("gbk"))
    n = len(b) # 求出 b 的字节数
    c = bytearray(n*2)
    j = 0
    for i in range(0, n):
        b1 = b[i]
        b2 = b1 ^ key # b1 = b2^ key
        c1 = b2 % 16
        c2 = b2 // 16 # b2 = c2*16 + c1
        c1 = c1 + 65
        c2 = c2 + 65 # c1,c2都是0~15之间的数,加上65就变成了A-P 的字符的编码
        c[j] = c1
        c[j+1] = c2
        j = j+2

    return c.decode("gbk")

def decrypt(key, tmp_str):
    '''
    解密算法
    :param key: 配合解密的key
    :param tmp_str: 待解密密的str
    :return: '' 解码失败 | 'xxx' 成功
    '''
    c = bytearray(str(tmp_str).encode("gbk"))
    n = len(c) # 计算 b 的字节数
    if n % 2 != 0 :
        return ''

    n = n // 2
    b = bytearray(n)
    j = 0
    for i in range(0, n):
        c1 = c[j]
        c2 = c[j+1]
        j = j+2
        c1 = c1 - 65
        c2 = c2 - 65
        b2 = c2*16 + c1
        b1 = b2^ key
        b[i]= b1
    try:
        return b.decode("gbk")
    except:
        return ''

def md5_encrypt(target_str, encoding='utf-8'):
    '''
    得到md5加密的字符串
    :param target_str:
    :param encoding:
    :return:
    '''
    _ = md5()
    _.update(target_str.encode(encoding=encoding))

    result = _.hexdigest()

    return result

def get_uuid1() -> str:
    '''
    根据时间戳等, 随机生成一个唯一的uuid
    :return:
    '''
    return str(uuid1())

def get_uuid3(target_str) -> str:
    '''
    make a UUID using an MD5 hash of a namespace UUID and a name(唯一的识别码)
    :param target_str:
    :return: str
    '''
    return str(uuid3(NAMESPACE_DNS, target_str))