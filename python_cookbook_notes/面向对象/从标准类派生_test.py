# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-23 下午2:38
# @File    : 从标准类派生_test.py

# 不可变类型的例子
# 我们覆盖了__new__()特殊方法来定制我们的对象
# 使之与python标准的浮点型(float)有一些区别: 我们使用round()内建函数对原浮点型进行舍入操作
class RoundFloat(float):
    def __new__(cls, val):
        return float.__new__(cls, round(val, 2))

# 通常情况下最好是适用super()内建函数来捕获对应父类以调用它的父方法
class RoundFloat2(float):
    def __new__(cls, val):
        return super(RoundFloat2, cls).__new__(cls, round(val, 2))

print(RoundFloat2(1.5955))
print(RoundFloat2(1.5945))
print(RoundFloat2(-1.9955))

# 可变类型的例子
# 子类化一个可变类型与此类似, 你可能不需要使用__new__()(或甚至__init__())
# 因为通常设置不多,一般情况下,你所继承到的类型的默认行为就是你想要的
# 下面创建一个新的字典类型,它的keys()方法会自动排序结果
class SortKeyDict(dict):
    def keys(self):
        return sorted(super(SortKeyDict, self).keys())

# 一定要谨慎,而且意识到你正在干什么


