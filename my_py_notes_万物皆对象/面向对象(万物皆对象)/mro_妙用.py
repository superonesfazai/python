# coding:utf-8

'''
@author = super_fazai
@File    : mro_妙用.py
@connect : superonesfazai@gmail.com
'''

from pprint import pprint

# mro方法就是这个类型所继承的父类的列表

print(1..__class__.__mro__)     # (<class 'float'>, <class 'object'>)
print(''.__class__.__mro__)     # (<class 'str'>, <class 'object'>)

# 通过这种方法,我们可以得到一些类型的对象,这个对于一些限制极严的情况下有很大的用处,
# 比如说open以及其他文件操作的函数和类型被过滤了的情况下我们可以使用如下的方法来打开文件

'''
** 在Python里，这段[].__class__.__mro__[-1].__subclasses__()魔术代码，不用import任何模块，但可调用任意模块的方法
'''

def read_file(file_name):
    # for index, i in enumerate("".__class__.__mro__[-1].__subclasses__()):
    #     print(index, i)

    return "".__class__.__mro__[-1].__subclasses__()[40](file_name).read()

# print(read_file(file_name='./__init__.py'))

print([].__class__.__mro__[-1].__subclasses__())

# 查看哪些内置函数可以利用
print(dir(__builtins__))
