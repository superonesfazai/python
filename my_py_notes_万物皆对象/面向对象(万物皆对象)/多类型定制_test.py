# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-23 下午4:28
# @File    : 多类型定制_test.py

# 创建一个新类 NumStr
class NumStr(object):
    def __init__(self, num=0, string=''):
        self.__num = num
        self.__string = string
    # 把顺序对的字符串表示形式确定为"[num::'str']",如果用户看到引号的字符串会更加直观,所以使用"%s"替换成"%r"
    # 这相当于调用repr()或使用单反引号来给出字符串的可求值版本
    def __str__(self):      # define for str()
        return '[%d :: %r]' % \
               (self.__num, self.__string)

    __repr__ = __str__

    # 加法操作
    def __add__(self, other):   # define for s+o
        if isinstance(other, NumStr):
            return self.__class__(self.__num + \
                                  other.__num,
                                  self.__string + other.__string)
        else:
            raise(TypeError,
                  'Illegal argument type for built-in operation')
    # 执行数值乘法和字符串操作
    def __mul__(self, num):     # define for o*n
        if isinstance(num, int):
            return self.__class__(self.__num * num,
                                  self.__string * num)
        else:
            raise(TypeError,
                  'Illegal argument type for built-in operation')
    # 返回一个布朗值
    def __nonzero__(self):      # False if both are
        return self.__num or len(self.__string)

    # 重载__cmp__()助手函数,目的是返回的正值转为1,负值转为-1
    def __norm_cval(self, cmpres):      # normalize cmp()
        return __cmp__(cmpres, 0)       # 原是cmp()但报错

    def __cmp__(self, other):       # define for cmp()
        return self.__norm_cval(cmp(self.__num, other.__num)) + \
            self.__norm_cval(cmp(self.__string, other.__string))

a = NumStr(3, 'foo')
b = NumStr(3, 'goo')
c = NumStr(2, 'foo')
d = NumStr()
e = NumStr(string='boo')
f = NumStr(1)

print(a)
print(b)
print(c)
print(d)
print(e)
print(f)

print('')

# print(a < b)
# print(b < c)
# print(a == a)
print(b * 2)
print(a * 3)
print(b + e)
print(e + b)

print('')

if d: 'not false'
if e: 'not false'

cmp(a, b)
cmp(a, c)
cmp(a, a)

