# coding = utf-8

'''
@author = super_fazai
@File    : 被装饰的函数有不定长参数_test.py
@Time    : 2017/8/5 22:12
@connect : superonesfazai@gmail.com
'''

from time import ctime, sleep

# 对应使用可变参数*args, 和关键字参数**kwargs来接收不同的参数即可
#可变参数
#可变参数就是传入的参数个数是可变的，可以是1个、2个到任意个，还可以是0个
#关键字参数
#关键字参数允许你传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict
def timefun(func):
    def wrappedfunc(*args, **kwargs):
        print("%s called at %s"%(func.__name__, ctime()))
        func(*args, **kwargs)
    return wrappedfunc

@timefun
def foo(a, b, c):
    print(a+b+c)

foo(3,5,7)
sleep(2)
foo(2,4,9)

@timefun
def foo2(**kwargs):
    total = 0
    for v in kwargs.values():
        total += v
    print(total)

tmp = {'a':1, 'b':2, 'c':3}
foo2(**tmp)     # 切记字典要这样传参才有效且不报错