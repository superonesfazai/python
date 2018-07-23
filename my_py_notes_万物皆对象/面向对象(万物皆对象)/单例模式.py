# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-26 上午11:09
# @File    : 单例模式.py

"""
单例模式的价值所在: 保证一个类只有一个实例，并提供一个访问它的全局访问点。它就可以严格地控制客户怎样访问它以及何时访问它。
    当一个类只允许创建一个实例时，可以考虑使用单例模式。
"""

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
            print('-' * 5)

s1 = Singleton()
s1.type = "动漫人物"
print(s1.type)
s2 = Singleton()
print(s2.type)

'''
__new__和__init__的区别：
    1. __new__是一个静态方法, 而__init__是一个实例方法
    2. __new__方法会返回一个创建的实例, 而__init__什么都不返回
    3. 只有在__new__返回一个cls的实例时后面的__init__才能被调用
    4. 当创建一个新实例时调用__new__, 初始化一个实例时用__init__
'''