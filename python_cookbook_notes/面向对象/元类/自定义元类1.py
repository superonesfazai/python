# coding = utf-8

'''
@author = super_fazai
@File    : 自定义元类1.py
@Time    : 2017/8/6 17:11
@connect : superonesfazai@gmail.com
'''

# 元类的主要目的就是为了当创建类时能够自动地改变类
# 通常你会为API做这样的事情, 你希望可以创建符合当前上下文的类

'''
假想⼀个很傻的例⼦, 你决定在你的模块⾥所有的类的属性都应该是⼤写形式. 
有好⼏种⽅法可以办到, 但其中⼀种就是通过在模块级别设定__metaclass__
采⽤这种⽅法, 这个模块中的所有类都会通过这个元类来创建
我们只需要告诉元类把所有的属性都改成⼤写形式就万事⼤吉了
'''
# 幸运的是, __metaclass__实际上可以被任意调⽤
# 它并不需要是⼀个正式的类, 所以, 我这⾥就先以⼀个简单的函数作为例⼦开始

## 等同于: Foo = upper_attr(future_class_name, future_class_parents, future_class_attr)

# 在python3中
def upper_attr(future_class_name, future_class_parents, future_class_attr):
    # 遍历属性字典, 把不是__开头的属性名字变为大写
    new_attr = {}
    for name, value in future_class_attr.items():
        if not name.startswith('__'):
            new_attr[name.upper()] = value
    # 调用type来创建一个类
    return type(future_class_name, future_class_parents, new_attr)

class Foo(object, metaclass=upper_attr):
    bar = 'bip'

print(hasattr(Foo, 'bar'))      # 输出False
print(hasattr(Foo, 'BAR'))      # 输出True

f = Foo()
print(f.BAR)                    # 输出bip

# 在python2中, __metaclass__被当作属性来赋值使用
'''
def upper_attr(future_class_name, future_class_parents, future_class_attr):
    #遍历属性字典， 把不是__开头的属性名字变为⼤写
    newAttr = {}
    for name,value in future_class_attr.items():
        if not name.startswith("__"):
            newAttr[name.upper()] = value
            #调⽤type来创建⼀个类
    return type(future_class_name, future_class_parents, newAttr)

class Foo(object):
    __metaclass__ = upper_attr #设置Foo类的元类为upper_attr
    bar = 'bip'

print(hasattr(Foo, 'bar'))
print(hasattr(Foo, 'BAR'))
f = Foo()
print(f.BAR)
'''