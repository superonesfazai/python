# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-23 下午2:10
# @File    : 函数修饰符_test.py

class TestStaticMethod:
    @staticmethod
    def foo():
        print('calling static method foo()')

class TestClassMethod:
    @classmethod
    def foo(cls):
        print('call class method foo()')
        print('foo() is part of class:', cls.__name__)

test1 = TestStaticMethod()
test1.foo()

test2 = TestClassMethod()
test2.foo()