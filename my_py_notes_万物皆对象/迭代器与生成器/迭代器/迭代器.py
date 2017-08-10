# coding = utf-8

class MyList(object):
    '''自定义一个容器, 保存多个数据, 做成可迭代对象'''
    def __init__(self):
        self.container = []     # container中文意思为容器

    def add(self, item):
        '''用来填充数据'''
        self.container.append(item)

    def __iter__(self):
        '''返回一个迭代器对象'''
        return MyIterator(self.container)

    def obj_fun(self):
        # 对象方法
        # 通过self可以操作对象属性, 类属性(但不能修改)
        pass
    @classmethod
    def class_fun(cls):
        # 类方法
        # 通过cls只能操作类属性
        pass

    @staticmethod
    def static_fun():
        # 静态方法
        # 如果不借助类名的方法, 那么即不能操作类属性, 也不能操作对象属性
        pass

class MyIterator(object):
    '''自定义迭代器'''
    # i = 0     需要定义为对象属性，因为每次迭代新建一个对象, i是独立的, 所以不是类属性
    def __init__(self, container):
        self.index = 0
        self.container = container

    def __next__(self):     # 实现迭代
        if self.index < len(self.container):
            # print(len(self.container))
            item = self.container[self.index]
            self.index += 1
            return item
        else:
            raise StopIteration

    def __iter__(self):
        return self     # 本身已经为一个迭代器, 所以返回自身

my_list1 = MyList()
my_list1.add(100)
my_list1.add(200)
my_list1.add(300)

my_iterator = my_list1.__iter__()
print(my_iterator.__next__())
print(my_iterator.__next__())
print(my_iterator.__next__())

# iterator = my_list1.__iter__()
# iterator.__next__()     # 100
# iterator.__next__()     # 200


# 为了实现下面的方法, 自己写一个迭代器
# for num in my_list1:
#     print(num)

# 数据   属性   类属性   对象属性

# 函数   方法   对象方法    类方法     静态方法

