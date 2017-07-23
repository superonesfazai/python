# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-23 下午5:24
# @File    : 简单的包装类_test.py

# 下面这个类几乎可以包装任何对象,提供基本功能
class WrapMe(object):
    def __init__(self, obj):
        self.__data = obj

    def get(self):
        return self.__data

    def __repr__(self):
        return 'self.__data'

    def __str__(self):
        return str(self.__data)

    def __getattr__(self, item):
        return getattr(self.__data, item)

wrapped_complex = WrapMe(3.5 + 4.2j)
print(wrapped_complex)      # 包装对象: repr()
print(wrapped_complex.real)     # 实部属性
print(wrapped_complex.imag)     # 虚部属性
print(wrapped_complex.conjugate())     # conjugate()方法
print(wrapped_complex.get())    # 实例对象