# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-24 上午8:45
# @File    : 静态方法_类方法_test.py

# 类方法: 是类对象所拥有的方法
# 需要用修饰器@classmethod来标识其为类方法
# 对于类方法,
# 第一个参数必须是类对象
# 一般以cls作为第一个参数(当然可以用其他名称的变量作为其第一个参数,但是大部分人都习惯以'cls'作为第一个参数的名字，就最好用'cls'了)
# 能够通过实例对象和类对象去访问

class People(object):
    country = 'china'

    #类方法，用classmethod来进行修饰
    @classmethod
    def getCountry(cls):
        return cls.country

    @classmethod
    def setCountry(cls,country):
        cls.country = country


p = People()
print(p.getCountry())    #可以用过实例对象引用
print(People.getCountry())    #可以通过类对象引用

p.setCountry('japan')

print(p.getCountry())
print(People.getCountry())

print('')

# 静态方法
# 需要通过修饰器@staticmethod来进行修饰
# 静态方法不需要多定义参数
class People(object):
    country = 'china'

    @staticmethod
    #静态方法
    def getCountry():
        return People.country


print(People.getCountry())

'''
从类方法和实例方法以及静态方法的定义形式就可以看出来
类方法的第一个参数是类对象cls
那么通过cls引用的必定是类对象的属性和方法；而实例方法的第一个参数是实例对象self
那么通过self引用的可能是类属性
也有可能是实例属性（这个需要具体分析）
不过在存在相同名称的类属性和实例属性的情况下
实例属性优先级更高
静态方法中不需要额外定义参数
因此在静态方法中引用类属性的话
必须通过类对象来引用
'''