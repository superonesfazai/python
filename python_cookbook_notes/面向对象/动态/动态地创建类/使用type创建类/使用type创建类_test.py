# coding = utf-8

'''
@author = super_fazai
@File    : 使用type创建类_test.py
@Time    : 2017/8/6 15:57
@connect : superonesfazai@gmail.com
'''

# type还有一种完全不同的功能, 动态的创建类
# type可以接受一个类的描述作为参数, 然后返回一个类(要知道, 根据传⼊参数的不同, 同⼀个函数拥有两种完全不同的⽤法是⼀件很傻的事情, 但这在Python中是为了保持向后兼容性)
# type的工作方式:
# type(类名, 由父类名称组成的元组(针对继承的情况可以留空), 包含属性的字典(名称和值))

Test = type('Test', (), {})     # 我们使⽤"Test"作为类名, 并且也可以把它当做⼀个变量来作为类的引⽤
print(Test)
print(help(Test))

'''
注意：
1. type的第2个参数， 元组中是⽗类的名字， ⽽不是字符串
2. 添加的属性是类属性， 并不是实例属性
'''

'''
测试结果:
<class '__main__.Test'>
Help on class Test in module __main__:

class Test(builtins.object)
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)

None
'''