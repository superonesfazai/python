# coding = utf-8

'''
@author = super_fazai
@File    : 使用property升级getter和setter方法.py
@Time    : 2017/8/6 12:41
@connect : superonesfazai@gmail.com
'''

# 通过property函数给实例属性 实现设置值和获取值的方法
class Money(object):
    def __init__(self):
        self.__money = 0

    def getMoney(self):
        return self.__money

    def setMoney(self, value):
        if isinstance(value, int):
            self.__money = value
        else:
            print("error:不是整型数字")

    money = property(getMoney, setMoney)    # 定义一个属性, 当对这个money设置值时调用setMoney, 获取值时调用getMoney
                                            # property传参有顺序限制, 必须先是getter方法, 再是setter方法

a = Money()
a.money = 100       # 调用setMoney()
print(a.money)      # 调用getMoney()
#100