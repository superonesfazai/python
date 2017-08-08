# coding = utf-8

'''
@author = super_fazai
@File    : 装饰器带参数_在原有装饰器的基础上_设置外部变量.py
@Time    : 2017/8/5 22:47
@connect : superonesfazai@gmail.com
'''

from time import ctime, sleep

# 功能: 通过给一个装饰器外层再加一个装饰器(这个装饰器带有的参数用来给内部装饰器判断或使用内部装饰器的对应功能)

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

# 通过装饰器带参数,对应打印需求的log功能
def set_log(pre='F'):
    def log(func):
        def inner(*args, **kwargs):
            nonlocal pre
            # print(tmp)
            if pre == 'T':
                print("%s called at %s" % (func.__name__, ctime()))
                result = func()
                pre = 'done'
                print(pre)
                return result

            elif pre == 'F':
                print("%s called at %s" % (func.__name__, ctime()))
                return func()
                print(ctime())
                pre = 'done'

        return inner
    return log

@set_log('T')
def say_hello():
    print('hello')

say_hello()

'''
测试结果:
foo called at Sun Aug  6 12:13:59 2017 itcast
I am foo
foo called at Sun Aug  6 12:14:01 2017 itcast
I am foo
too called at Sun Aug  6 12:14:01 2017 python
I am too
too called at Sun Aug  6 12:14:03 2017 python
I am too
say_hello called at Sun Aug  6 12:14:03 2017
hello
done
'''