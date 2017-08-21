# coding = utf-8

from random import randint
'''
@author = super_fazai
@File    : 闭包_test1.py
@Time    : 2017/8/4 11:21
@connect : superonesfazai@gmail.com
'''
# 闭包最外层相当于创建了一个函数对象, 内部是函数对象的方法
# 闭包最外层的参数和属性相当于类属性, 能被函数对象的方法绑定和调用
# 定义⼀个函数
def test(number):
    # 在函数内部再定义⼀个函数， 并且这个函数⽤到了外边函数的变量， 那么将这个函数以及⽤到的⼀些变量称之为闭包
    def test_in(number_in):
        print("in test_in 函数, number_in is %d" % number_in)
        return number+number_in
    # 其实这⾥返回的就是闭包的结果
    return test_in

# 给test函数赋值， 这个20就是给参数number
ret = test(20)
# 注意这⾥的100其实给参数number_in
print(ret(100))
# 注意这⾥的200其实给参数number_in
print(ret(200))

print('')

def outter(num):
    def inner(a):
        print(a+num)
    def inner0(b):
        print(b)
    def inner1():
        print('-' * 20)
    return inner

fun = outter(100)
fun(1)
fun(2)
getattr(fun, 'inner1')