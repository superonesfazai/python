# coding = utf-8

'''
@author = super_fazai
@File    : 装饰器带参数_在原有装饰器的基础上_设置外部变量.py
@Time    : 2017/8/5 22:47
@connect : superonesfazai@gmail.com
'''

from time import ctime, sleep

# 装饰器带参数的实现方法, 即在原有装饰器的基础上, 设置外部变量就可实现
def timefun_arg(pre="hello"):
    def timefun(func):
        def wrappedfunc():
            print("%s called at %s %s"%(func.__name__, ctime(), pre))
            return func()
        return wrappedfunc
    return timefun

@timefun_arg("itcast")
def foo():
    print("I am foo")

@timefun_arg("python")
def too():
    print("I am too")

foo()
sleep(2)
foo()
too()
sleep(2)
too()

'''
测试结果:
foo called at Sat Aug  5 22:52:14 2017 itcast
I am foo
foo called at Sat Aug  5 22:52:16 2017 itcast
I am foo
too called at Sat Aug  5 22:52:16 2017 python
I am too
too called at Sat Aug  5 22:52:18 2017 python
I am too
'''