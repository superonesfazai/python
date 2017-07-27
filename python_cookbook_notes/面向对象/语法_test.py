# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-26 下午8:13
# @File    : 语法_test.py

# 类属性只能通过类对象修改,实例属性只能通过实例对象修改
class a(object):
    __tmp_a = 'aa'

    def __init__(self, a='-'):
        self.__a = a

    # 返回类属性的值
    @classmethod
    def get_value(cls):
        return cls.__tmp_a

    @classmethod
    def set_instance_value(cls):
        cls.__a = 'b'
        return cls.__a

    def get_instance_value(self):
        return self.__a

    def set_value(self):
        self.__tmp_a = 'bb'

_a = a('a')
print(_a)
print(a.get_value())

_a.set_value()          # 尝试用实例对象的实例方法修改类属性,修改失败
print(a.get_value())

c = a.set_instance_value()  # 尝试用类对象的类方法修改实例对象的属性,修改成功但是不是实例对象
print(c)
print(_a.get_value())       # 实例对象的属性不变