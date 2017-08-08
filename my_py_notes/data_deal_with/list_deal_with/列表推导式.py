#coding:utf-8

'''
列表推导式为从序列中创建列表提供了一个简单的方法
普通的应用程式通过将一些操作应用于序列的每个成员并通过返回的元素创建列表
或者通过满足特定条件的元素创建子序列
'''

#例如, 假设我们创建一个 squares 列表
squares = []
for x in range(10):
    squares.append(x**2)
print(squares)
#注意这个 for 循环中的被创建(或被重写)的名为 x 的变量在循环完毕后依然存在

#使用如下方法,我们可以计算squares的值而不会产生任何的副作用
squares = list(map(lambda x: x**2, range(10)))
print(squares)
#或者等价于
squares = [x**2 for x in range(10)]
print(squares)
#上面这个方法更加简明且易读

#例如,如下的列表推导式结合两个列表的元素,如果元素之间不相等的话
list = [(x, y) for x in [1, 2, 3] for y in [3, 1, 4] if x != y]
print(list)

#此外列表推导式可使用复杂的表达式和嵌套函数
from math import pi
list = [str(round(pi, i)) for i in range(1, 6)]
print(list)