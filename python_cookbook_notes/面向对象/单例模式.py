# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-26 上午11:09
# @File    : 单例模式.py

# 实例化一个单例
class Singleton:
    __instance = None  # 保存创建首次创建的对象

    def __new__(cls):
        if cls.__instance is None:
            print("创建对象")
            cls.__instance = super().__new__(cls)
        return cls.__instance


s1 = Singleton()
print(s1)
s2 = Singleton()
print(s2)

print('')

# 创建单例时，只执行1次__init__方法
class Singleton:
    __instance = None  # 保存创建首次创建的对象
    __has_init = False  # 记录是否已经初始化

    def __new__(cls):   # 对于单例模式,只需要创建一次对象
        if cls.__instance is None:
            print("创建对象")
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):   # 对于单例模式,只需要一次对象初始化
        if not self.__has_init:
            print("对象初始化")
            self.type = "猫"
            self.__has_init = True

s1 = Singleton()
s1.type = "动漫人物"
print(s1.type)
s2 = Singleton()
print(s2.type)