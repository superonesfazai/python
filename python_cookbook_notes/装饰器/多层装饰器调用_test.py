# coding = utf-8

'''
@author = super_fazai
@File    : 多层装饰器调用_test.py
@Time    : 2017/8/6 08:54
@connect : superonesfazai@gmail.com
'''

def itcast1(fun):
    def inner():
        print('itcast1 start')
        fun()
        print('itcast1 end')
    return inner

def itcast2(fun):
    def inner():
        print('itcast2 start')
        fun()
        print('itcast2 end')
    return inner

# say_hello = itcast1(itcast2(say_hello))
# 一层一层的拆    执行->到itcast1的func的前一行code->跳到itcast2直到itcast2装饰器执行完毕并返回结果->跳到itcast1继续执行func下一行code(直到itcase1执行完毕)
# 先执行itcast1 直到执行到itcast1中的func，因为itcast1中的say_hello()被itcast2装饰
# 所以再先执行itcast2来得到返回值
# 从而继续执行itcast1
@itcast1
@itcast2
def say_hello():
    print('hello')

say_hello()

'''
测试结果:
itcast1 start
itcast2 start
hello
itcast2 end
itcast1 end
'''

