# coding = utf-8

'''
@author = super_fazai
@File    : 自定义元类2.py
@Time    : 2017/8/6 17:39
@connect : superonesfazai@gmail.com
'''

class UpperAttrMetaClass(type):
    # __new__ 是在__init__之前被调⽤的特殊⽅法
    # __new__是⽤来创建对象并返回之的⽅法
    # ⽽__init__只是⽤来将传⼊的参数初始化给对象
    # 你很少⽤到__new__, 除⾮你希望能够控制对象的创建
    # 这⾥, 创建的对象是类, 我们希望能够⾃定义它, 所以我们这⾥改写__new__
    # 如果你希望的话, 你也可以在__init__中做些事情
    # 还有⼀些⾼级的⽤法会涉及到改写__call__特殊⽅法, 但是我们这⾥不⽤
    def __new__(cls, future_class_name, future_class_parents, future_class_attr):
        #遍历属性字典, 把不是__开头的属性名字变为⼤写
        newAttr = {}
        for name,value in future_class_attr.items():
            if not name.startswith("__"):
                newAttr[name.upper()] = value
        # 重点:
        # ⽅法1: 通过'type'来做类对象的创建
        # return type(future_class_name, future_class_parents, newAttr)
        # ⽅法2: 复⽤type.__new__⽅法
        # 这就是基本的OOP编程, 没什么魔法
        # return type.__new__(cls, future_class_name, future_class_parents, newAttr)
        # ⽅法3: 使⽤super⽅法
        return super(UpperAttrMetaClass, cls).__new__(cls, future_class_name, future_class_parents, newAttr)

class Foo(object, metaclass=UpperAttrMetaClass):
    bar = 'bip'

print(hasattr(Foo, 'bar'))      # 输出: False
print(hasattr(Foo, 'BAR'))      # 输出:True

f = Foo()
print(f.BAR)                    # 输出:'bip

'''
就是这样, 除此之外, 关于元类真的没有别的可说的了。 
但就元类本身⽽⾔, 它们其实是很简单的：
1. 拦截类的创建
2. 修改类
3. 返回修改之后的类
'''