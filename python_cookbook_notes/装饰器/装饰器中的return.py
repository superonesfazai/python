# coding = utf-8

'''
@author = super_fazai
@File    : 装饰器中的return.py
@Time    : 2017/8/5 22:30
@connect : superonesfazai@gmail.com
'''
from time import ctime, sleep

def timefun(func):
    def wrappedfunc():
        print("%s called at %s"%(func.__name__, ctime()))
        func()
    return wrappedfunc

# 总结:
# 一般情况下为了让修饰器更通用, 可以有return
def timefun2(func):
    def wrappedfunc():
        print("%s called at %s"%(func.__name__, ctime()))
        return func()   # 就可以调用含return的普通函数了
    return wrappedfunc

@timefun
def foo():
    print("I am foo")

@timefun
def getInfo():
    return '----hahah---'

@timefun2
def getInfo2():
    return '----hahah---'

foo()
sleep(2)
foo()
print(getInfo())

print()

foo()
sleep(2)
foo()
print(getInfo2())

# 因为装饰器timefun返回的是一个函数对象
# 而非一个执行过程  eg: wrappedfunc()
# 总结:
# 一般情况下为了让修饰器更通用, 可以有return
'''
测试结果:
foo called at Sat Aug  5 22:44:10 2017
I am foo
foo called at Sat Aug  5 22:44:12 2017
I am foo
getInfo called at Sat Aug  5 22:44:12 2017
None

foo called at Sat Aug  5 22:44:12 2017
I am foo
foo called at Sat Aug  5 22:44:14 2017
I am foo
getInfo2 called at Sat Aug  5 22:44:14 2017
----hahah---
'''