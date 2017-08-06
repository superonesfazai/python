# coding = utf-8

'''
@author = super_fazai
@File    : 使用property取代getter和setter.py
@Time    : 2017/8/6 12:46
@connect : superonesfazai@gmail.com
'''

# 使用装饰器形式的property为实例属性实现设置值, 和获取值
class Money(object):
    def __init__(self):
        self.__money = 0
    # 使用装饰器对money进行装饰, 那么会自动添加一个叫money的属性, 当调用获取money的值时, 调用此下一行的方法
    @property
    def money(self):
        return self.__money

    # 使用装饰器对money进行装饰, 当对money设置值时, 调用下一行的方法
    @money.setter
    def money(self, value):
        if isinstance(value, int):
            self.__money = value
        else:
            print("error:不是整型数字")

a = Money()
a.money = 100
print(a.money)

