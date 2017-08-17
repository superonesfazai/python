# coding = utf-8

# 迭代器(Iterator)
# 具备了__next__方法
# 可迭代对象
# 一个对象如果具备了__iter__方法的对象是可迭代对象
# isinstance(),用于判断是否为可迭代对象

from collections import Iterable

print(isinstance([], Iterable))     # True

# 测试发现添加了__iter__方法的my_list对象已经是一个可迭代对象了
class MyList(object):
    def __init__(self):
        self.container = []

    def add(self, item):
        self.container.append(item)

    def __iter__(self):     # __iter__方法会返回一个对象
        '''返回一个迭代器'''
        # 暂时忽略如何构造一个迭代器对象
        pass

my_list = MyList()
from collections import Iterable
print(isinstance(my_list, Iterable))        # True

# for循环的本质如下:
'''
    1. 调用可迭代对象的__iter__()方法返回一个可迭代对象
    2. 对迭代器对象调用__next__()方法
        如果未捕获StopIteration异常, 表示未迭代结束
        如果抛出异常, 迭代结束
    3. 执行循环体代码
    4. 跳转到步骤2执行
'''
li = [1, 2, 3]
iterator = li.__iter__()

print(isinstance(iter([]), Iterable))       # True

while True:
    try:
        num = iterator.__next__()
    except StopIteration as e:
        break
    else:
        print(num)

print('')

