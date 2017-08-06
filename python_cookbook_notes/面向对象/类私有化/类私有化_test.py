# coding = utf-8

'''
@author = super_fazai
@File    : 类私有化_test.py
@Time    : 2017/8/6 12:21
@connect : superonesfazai@gmail.com
'''

class Person(object):
    def __init__(self, name, age, taste):
        self.name = name
        self._age = age
        self.__taste = taste
    def showperson(self):
        print(self.name)
        print(self._age)
        print(self.__taste)
    def dowork(self):
        self._work()
        self.__away()
    def _work(self):
        print('my _work')
    def __away(self):
        print('my __away')

class Student(Person):
    def construction(self, name, age, taste):
        self.name = name
        self._age = age
        self.__taste = taste
    def showstudent(self):
        print(self.name)
        print(self._age)
        print(self.__taste)
    @staticmethod
    def testbug():
        _Bug.showbug()

# 模块内可以导入, 当from cur_module import *时, 不导入
class _Bug(object):
    @staticmethod
    def showbug():
        print("showbug")

s1 = Student('jack', 25, 'football')
s1.showperson()
print('*'*20)

# 无法访问__taste, 导致报错
#s1.showstudent()
s1.construction('rose', 30, 'basketball')
s1.showperson()
print('*'*20)
s1.showstudent()
print('*'*20)
Student.testbug()

'''
测试结果:
jack
25
football
********************
rose
30
football
********************
rose
30
basketball
********************
showbug
'''