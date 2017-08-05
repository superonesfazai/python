# coding = utf-8

'''
@author = super_fazai
@File    : 被装饰的函数有参数_test.py
@Time    : 2017/8/5 22:07
@connect : superonesfazai@gmail.com
'''
# 有什么参数就对应声名并接收什么参数即可

from time import ctime, sleep
def timefun(func):
    def wrappedfunc(a, b):
        print("%s called at %s"%(func.__name__, ctime()))
        print(a, b)
        func(a, b)
    return wrappedfunc

@timefun
def foo(a, b):
    print(a+b)

foo(3,5)
sleep(2)
foo(2,4)

