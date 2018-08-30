# coding:utf-8

'''
@author = super_fazai
@File    : python的伪private属性和函数.py
@connect : superonesfazai@gmail.com
'''

"""
在java,c++等其他一些面向对象的语言中,有着严格的访问权限控制,Private函数是不可能在域外访问的.

python中也有着类似的机制:
在一个类中,以双下划线开头的函数和属性是Private的,
但是这种Private并不是真正的,而只是形式上的,
用于告诉程序员,这个函数不应该在本类之外的地方进行访问,而是否遵守则取决于程序员的实现
"""

from pprint import pprint

class A():
    __a = 1
    b = 2
    def __c(self):
        print('asd')

    def d(self):
        print('fgh')

# 从dir的结果,可以看出来,公有的函数和属性,使用其名字直接进行访问,而私有的属性和函数,使用 下划线+类名+函数名访问即可
print(A)
pprint(dir(A))
print(A._A__a)
_ = A()
print(_._A__c())