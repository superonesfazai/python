# coding = utf-8

'''
@author = super_fazai
@File    : 迭代器2.py
@Time    : 2017/8/3 13:58
@connect : superonesfazai@gmail.com
'''

class MyList(object):
    '''自定义一个容器, 保存多个数据, 做成可迭代对象'''
    def __init__(self):
        self.container = []     # container中文意思为容器
        self.index = 0
    def add(self, item):
        '''用来填充数据'''
        self.container.append(item)

    def __iter__(self):
        '''返回一个迭代器对象'''
        return self     # 返回本身, 因为本身就是迭代器了

    def __next__(self):     # 实现迭代
        if self.index < len(self.container):
            # print(len(self.container))
            item = self.container[self.index]
            self.index += 1
            return item
        else:
            raise StopIteration

my_list1 = MyList()
my_list1.add(100)
my_list1.add(200)
my_list1.add(300)

# my_iterator = my_list1.__iter__()
# print(my_iterator.__next__())
# print(my_iterator.__next__())
# print(my_iterator.__next__())

print(my_list1.__next__())
print(my_list1.__next__())
print(my_list1.__next__())
print(my_list1.__next__())

# iterator = my_list1.__iter__()
# iterator.__next__()     # 100
# iterator.__next__()     # 200


# 为了实现下面的方法, 自己写一个迭代器
# for num in my_list1:
#     print(num)

# 数据   属性   类属性   对象属性

# 函数   方法   对象方法    类方法     静态方法

