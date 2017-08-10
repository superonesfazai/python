# coding = utf-8

'''
@author = super_fazai
@File    : 使用type创建带有方法的类.py
@Time    : 2017/8/6 16:14
@connect : superonesfazai@gmail.com
'''

'''
在Python中, 类也是对象, 你可以动态的创建类 
这就是当你使⽤关键字class时Python在幕后做的事情, ⽽这就是通过元类来实现的
'''

# 只需要定义一个有着恰当签名的函数并将其作为属性赋值就可以了

Foo = type('Foo', (), {'bar':True})
# 添加实例方法
def echo_bar(self):     # 定义了一个普通的函数
    print(self.bar)

Foo_child = type('Foo_child', (Foo,), {'echo_bar':echo_bar})
print(hasattr(Foo, 'echo_bar'))
print(hasattr(Foo_child, 'echo_bar'))

my_foo = Foo_child()
my_foo.echo_bar()

print('-' * 20)

# 添加静态方法
@staticmethod
def test_static():
    print('static method...')

Foo_child = type('Foo_child', (Foo,), {'echo_bar':echo_bar, 'test_static':test_static})
foo_child = Foo_child()
print(foo_child.test_static)
foo_child.test_static()
foo_child.echo_bar()

print('-' * 20)

# 添加类方法
@classmethod
def test_class(cls):
    print(cls.bar)

Foo_child = type('Foo_child', (Foo,), {'echo_bar':echo_bar, 'test_static':test_static, 'test_class':test_class})
foo_child = Foo_child()
foo_child.test_static()

print('-' * 20)

class A(object):
    num = 100

def print_b(self):
    print(self.num)

@staticmethod
def print_static():
    print("----haha-----")

@classmethod
def print_class(cls):
    print(cls.num)

B = type("B", (A,), {"print_b":print_b, "print_static":print_static, "print_class":print_class})
b = B()
b.print_b()
b.print_static()
b.print_class()

'''
测试结果:
False
True
True
--------------------
<function test_static at 0x1010bd950>
static method...
True
--------------------
static method...
--------------------
100
----haha-----
100
'''
