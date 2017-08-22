# coding = utf-8

'''
@author = super_fazai
@File    : 运行过程中动态给类绑定属性_方法.py
@Time    : 2017/8/6 09:47
@connect : superonesfazai@gmail.com
'''

'''
既然给类添加方法, 是使用 类名.方法名 = xxx  
那么给对象添加方法也类似于 类名.方法名 = xxx
'''
import types

class Person(object):
    num = 0
    def __init__(self, name = None, age = None):
        self.name = name
        self.age = age
    def eat(self):
        print("eat food")

# 定义一个实例方法
def run(self, speed):
    print("%s在移动, 速度是 %d km/h" % (self.name, speed))

# 定义一个类方法
@classmethod
def testClass(cls):
    cls.num = 100

# 定义一个静态方法
@staticmethod
def testStatic():
    print("---static method----")

P = Person("老王", 24)    # 创建一个实例对象
P.eat()                  # 调用在class中的方法

# 给这个对象添加实例方法
P.run = types.MethodType(run, P)
P.run(180)               # 调用实例方法

# 给Person类绑定类方法
Person.testClass = testClass
# 调用类方法
print(Person.num)
Person.testClass()
print(Person.num)

# 给Person绑定静态方法
Person.testStatic = testStatic
# 调用静态方法
Person.testStatic()

'''
测试结果:
eat food
老王在移动, 速度是 180 km/h
0
100
---static method----
'''