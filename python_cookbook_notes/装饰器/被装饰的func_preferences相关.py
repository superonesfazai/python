# coding = utf-8

'''
@author = super_fazai
@File    : 被装饰的func_preferences相关.py
@Time    : 2017/8/6 08:51
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
    "test function"
    print('I am test')

test()
print(test.__doc__)

print()
# 所以, python的functools提供了一个叫wraps的装饰器来消除这种副作用
import functools

def note(func):
    "note function"
    @functools.wraps(func)      # 对应传入想要恢复成的func属性
    def wrapper():
        "wrapper function"
        print('note something')
        return func()

    # 上面的@functions.warps(func)等同于下面给恢复属性, 但是前面的功能更强大不光光修改这两项, 所以还是用@functools.wraps(func)
    # wrapper.__name__ = func.__name__
    # wrapper.__doc__ = wrapper.__doc__
    return wrapper

@note
def test():
    "test function"
    print('I am test')

test()
print(test.__doc__)

'''
测试结果:
note something
I am test
wrapper function

note something
I am test
test function
'''
