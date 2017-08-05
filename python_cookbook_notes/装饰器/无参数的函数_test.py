# coding = utf-8

'''
@author = super_fazai
@File    : 无参数的函数_test.py
@Time    : 2017/8/5 21:58
@connect : superonesfazai@gmail.com
'''
from time import ctime, sleep

def timefun(func):
    def wrappedfunc():
        print('%s called at %s' % (func.__name__, ctime()))
        func()

    return wrappedfunc()

@timefun
def foo():
    print('I am foo')

foo()
sleep(3)
foo()

# 可以理解装饰器执行的行为为 foo = timefun(foo)
'''
foo先作为参数赋值给func后, foo接收指向timefun返回的wrappedfunc
foo()
# 调用foo(), 即等价于调用wrappedfunc()
'''