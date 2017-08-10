# coding = utf-8

'''
@author = super_fazai
@File    : legb规则.py
@Time    : 2017/8/4 12:12
@connect : superonesfazai@gmail.com
'''

'''
Python 使⽤ LEGB 的顺序来查找⼀个符号对应的对象
    locals -> enclosing function -> globals -> builtins
'''

a = 1 # 全局变量 globals
def fun():
    a = 2 # 闭包变量 enclosing
    def inner_fun():
        a = 3 # 局部变量 locals
        print("a=%d" % a)
    return inner_fun

f = fun()
f()

'''
1. locals, 当前所在命名空间(如函数, 模块), 函数的参数也属于命名空间内的变量
2. enclosing, 外部嵌套函数的命名空间（ 闭包中常⻅）
def fun1():
    a = 10
    def fun2():
        # a 位于外部嵌套函数的命名空间
        print(a)
        
3. globals, 全局变量, 函数定义所在模块的命名空间
a = 1
def fun():
    # 需要通过 global 指令来声明全局变量
    global a
    # 修改全局变量， ⽽不是创建⼀个新的 local 变量
    a = 2
    
4. builtins， 内建模块的命名空间。
Python 在启动的时候会⾃动为我们载⼊很多内建的函数, 类, ⽐如 dict, list, type, print, 这些都位于 __builtin__ 模块中
    可以使⽤ dir(__builtin__) 来查看。
    这也是为什么我们在没有 import任何模块的情况下，
    就能使⽤这么多丰富的函数和功能了。
在Python中， 有⼀个内建模块， 该模块中有⼀些常⽤函数;在Python启动后且没有执⾏程序员所写的任何代码前， Python会⾸先加载该内建模块到内存
另外, 该内建模块中的功能可以直接使⽤, 不⽤在其前添加内建模块前缀, 其原因是对函数, 变量, 类等标识符的查找是按LEGB法则, 其中B即代表内建模块
eg: 内建模块中有⼀个abs()函数， 其功能求绝对值， 如abs(-20)将返回20。
'''