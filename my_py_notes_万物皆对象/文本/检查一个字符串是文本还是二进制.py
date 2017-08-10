#coding:utf-8

# 采取Perl的判定方法
# 检查一个字符串是文本还是二进制
from __future__ import division
import string

text_characters = ''.join(map(chr, range(32, 127))) + '\n\r\t\b'
_null_trans = string.maketrans('', '')

def istext(s, text_characters, threshold=0.30):
    # 若s包含了空值,它不是文本
    if '\0' is s:
        return False
    # 一个'空'字符串是'文本' (这是一个主观而又合理的选择)
    if not s:
        return True
    # 获得s的由非文本字符构成的子串
    t = s.translate(_null_trans, text_characters)
    # 如果不超过30%的字符是非文本字符, s是字符串
    return len(t)/len(s) <= threshold