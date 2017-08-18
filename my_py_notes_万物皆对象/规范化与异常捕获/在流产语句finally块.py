# coding = utf-8

'''
@author = super_fazai
@File    : 在流产语句finally块.py
@Time    : 2017/8/18 21:33
@connect : superonesfazai@gmail.com
'''

"""
在此，try中的return, 在声明finally块简单地否决了在try块中的return，因为finally是保证一定会执行。所以，请谨慎使用finally块中的堕胎语句！
"""

# 例1:
def try_finally1():
    try:
        print('in try:')
        print('do some stuff')
        float('abc')
    except ValueError:
        print('an error occurred')
    else:
        print('no error occurred')
    finally:
        print('always execute finally')

try_finally1()

print('分割线'.center(40, '-'))

# 但是，您还可以猜测下一个代码单元将打印什么？
# 例2:
def try_finally2():
    try:
        print("do some stuff in try block")
        return "return from try block"
    finally:
        print("do some stuff in finally block")
        return "always execute finally"

print(try_finally2())

'''
测试结果:
in try:
do some stuff
an error occurred
always execute finally
------------------分割线-------------------
do some stuff in try block
do some stuff in finally block
always execute finally
'''