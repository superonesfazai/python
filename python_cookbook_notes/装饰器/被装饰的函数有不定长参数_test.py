# coding = utf-8

'''
@author = super_fazai
@File    : 被装饰的函数有不定长参数_test.py
@Time    : 2017/8/5 22:12
@connect : superonesfazai@gmail.com
'''

from time import ctime, sleep

# 对应使用可变参数*args, 和关键字参数**kwargs来接收不同的参数即可   (*args 为元组数据, **kwargs 为字典数据)
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

print()
print('----分割线----')
print()

@timefun
def foo2(*args, **kwargs):
    total = 0
    print('args = %s' % (args,))
    for k, v in kwargs.items():
        total += v
        print('k=', k, ' ', 'v=', v)
    print(total)
@timefun
def say_hello():        # 不传参数也能匹配到装饰器中的*args, **kwargs 即:*args = (), **kwargs = {}, 所以不报错, 同样使用了装饰器timefun
    print('---hello---')

say_hello()
a = (3, 4, 5)
tmp = {'a':1, 'b':2, 'c':3}
foo2(*a, **tmp)     # 切记字典要这样传参才有效且不报错
                    # * 跟 ** 代表打包

'''
测试结果:
foo called at Sun Aug  6 10:18:15 2017
15
foo called at Sun Aug  6 10:18:17 2017
15

----分割线----

say_hello called at Sun Aug  6 10:18:17 2017
---hello---
foo2 called at Sun Aug  6 10:18:17 2017
args = (3, 4, 5)
k= a   v= 1
k= b   v= 2
k= c   v= 3
6
'''