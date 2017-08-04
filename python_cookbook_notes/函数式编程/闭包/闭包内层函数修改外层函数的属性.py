# coding = utf-8

'''
@author = super_fazai
@File    : 闭包内层函数修改外层函数的属性.py
@Time    : 2017/8/4 11:57
@connect : superonesfazai@gmail.com
'''
# python3中的闭包修改全局变量方法
# 使用nonlocal在内层函数声名对应要修改的全局变量
def counter(start=0):
    def incr():
        nonlocal start
        start += 1
        return start
    return incr

c1 = counter(5)
print(c1())
print(c1())

c2 = counter(50)
print(c2())
print(c2())

print(c1())
print(c1())
print(c2())
print(c2())

# python2的⽅法
# 相当于在外层函数中创建一个可变对象eg:list, 然后在内层函数中修改可变对象的元素
'''
def counter(start=0):
    count=[start]
    def incr():
        count[0] += 1
        return count[0]
    return incr

c1 = counter(5)
print(c1())     #6
print(c1())     #7
c2 = counter(100)
print(c2())     #101
print(c2())     #102
'''