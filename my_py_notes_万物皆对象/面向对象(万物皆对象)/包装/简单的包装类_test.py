# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-23 下午5:24
# @File    : 简单的包装类_test.py

# 下面这个类几乎可以包装任何对象,提供基本功能
class WrapMe(object):
    def __init__(self, obj):
        self.__data = obj

    def get(self):
        return self.__data

    def __repr__(self):
        return 'self.__data'

    def __str__(self):
        return str(self.__data)

    def __getattr__(self, item):
        return getattr(self.__data, item)

wrapped_complex = WrapMe(3.5 + 4.2j)
print(wrapped_complex)      # 包装对象: repr()
print(wrapped_complex.real)     # 实部属性
print(wrapped_complex.imag)     # 虚部属性
print(wrapped_complex.conjugate())     # conjugate()方法
print(wrapped_complex.get())    # 实例对象

# 一旦我们创建了包装的对象类型,解释器调用repr(),就可得到一个字符串表示
# 然而我们继续访问复数的三种属性,我们在类中一种都没定义
# 实际上对这些对象的访问是通过getattr()方法,最终调用get()方法没有授权,因为它是为我们的对象定义的--它返回包装的真实的数据对象

print('')
# 下面使用我们的包装类用到一个list,我们将会创建对象,然后执行多种操作,每次授权给列表的方法
# 然而需要明白,只有已存在的属性是在此代码中授权的
# 特殊行为没有在类型的方法列表中,不能被访问,因为它们不是属性
# eg:对list的切片,内建议于类型中,而不是像append()方法那样作为属性存在,所以并不能通过__getitem__()特殊方法实现
wrapped_list = WrapMe([123, 'foo', 45.67])
wrapped_list.append('bar')
wrapped_list.append(123)
print(wrapped_list)
print(wrapped_list.index(45.67))
print(wrapped_list.count(123))
print(wrapped_list.pop())
print(wrapped_list)

try:
    print(wrapped_list[3])
except:
    print('AttributeError:__getitem__!')

print('')
# 但是我们有一种'作弊'行为
# get()方法返回一个对象,随后被索引以得到切片片段
real_list = wrapped_list.get()
print(real_list[3])
print(wrapped_list.get()[3])

print('')

f = WrapMe(open('避免死锁.md'))
print(f)
print(f.get())
print(f.readline())
print(f.tell)
f.seek(0)
print(f.readline())
f.close()
print(f.get())

# 一旦你熟悉了对象的属性,就能够开始理解一些信息片段从何而来,能够利用新得到的知识来重复功能
print('<%s file %s, mode %s at %x>' % (f.closed and 'closed' or 'open', 'f.name', 'f.mode', id(f.get())))

