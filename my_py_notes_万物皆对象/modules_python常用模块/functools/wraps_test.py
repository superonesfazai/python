# coding = utf-8

'''
@author = super_fazai
@File    : wraps_test.py
@Time    : 2017/8/6 09:09
@connect : superonesfazai@gmail.com
'''

'''
使用装饰器时, 有一些细节需要被注意
例如, 被装饰的函数其实已经是另外一个函数了(函数名函数属性会发生改变)
所以, python的functools提供了一个叫wraps的装饰器来消除这种副作用
'''

def note(func):
    "note function"
    def wrapper():
        "wrapper function"
        print('note something')
        return func()
    return wrapper

@note
def test():
    "避免死锁 function"
    print('I am 避免死锁')

test()
print(test.__doc__)

print()
# 所以, python的functools提供了一个叫wraps的装饰器来消除这种副作用
import functools

def note(func):
    "note function"
    @functools.wraps(func)
    def wrapper():
        "wrapper function"
        print('note something')
        return func()
    return wrapper

@note
def test():
    "避免死锁 function"
    print('I am 避免死锁')

test()
print(test.__doc__)

'''
测试结果:
note something
I am 避免死锁
wrapper function

note something
I am 避免死锁
避免死锁 function
'''