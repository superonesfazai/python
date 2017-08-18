# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-29 上午10:08
# @File    : 易面试点.py

# 1. 切记不要边遍历, 边增删, 否则会遗漏(即在循环时修改列表)
a = [11, 22, 33, 44, 55, 66]

for i in a:     # 丢失元素44
    print(i)
    if i == 33:
        a.remove(i)
print(a)
print('')

a = [11, 22, 33, 44, 55, 66]
# 边遍历边删除列表元素的一般步骤
# 解决方案: 先创建临时列表,用于记录要删除的元素,再遍历临时列表删除,并在原列表中删除
tmp = []
for i in a:
    if i == 33:
        tmp.append(i)
i = 0
for j in tmp:
    if i >0 and i < len(a)-1:
        print(a[i])
    else:
        break
    i += 1
    a.remove(j)

print(a)

print('分割线'.center(40, '-'))

# 2. 切记不要使用可变对象来作为函数的默认参数
# 您可能希望每次调用该函数时都会创建一个新的列表，而不提供默认参数的参数
# 但情况并非如此：Python将在第一次定义函数时创建可变对象（默认参数）不是当它被调用时

# 例1:
def append_to_list(value, def_list=[]):
    def_list.append(value)
    return def_list

my_list = append_to_list(1)
print(my_list)

my_other_list = append_to_list(2)
print(my_other_list)

# 例2:
# 另一个很好的例子表明，当创建函数（而不是调用它时）创建默认参数：
import time
def report_arg(my_default=time.time()):
    print(my_default)

report_arg()

time.sleep(2)

report_arg()

print('分割线'.center(40, '-'))

# 注意生成器的消耗
# 注意在将'in'检查与生成器组合时发生的情况，因为一旦一个位置被“消耗”，它们就不会从一开始就进行评估
# 我们可以将其转换为list 来避免这种情况
gen = (i for i in range(5))
print('2 in gen,', 2 in gen)        # True
print('3 in gen,', 3 in gen)        # True
print('1 in gen,', 1 in gen)        # False

# 尽管这样做会击败生成器的目的（在大多数情况下），我们可以将一个发电机转换成一个列表来规避这个问题
gen = (i for i in range(5))
gen = list(gen)
print('2 in gen,', 2 in gen)        # True
print('3 in gen,', 3 in gen)        # True
print('1 in gen,', 1 in gen)        # True

print('分割线'.center(40, '-'))

# bool是int的子类
print('isinstance(True, int):', isinstance(True, int))      # True
print('True + True:', True + True)                          # 2
print('3*True + True:', 3*True + True)                      # 4
print('3*True - False:', 3*True - False)                    # 3

# 关于lambda-in-closures-and-a-loop陷阱

print('分割线'.center(40, '-'))

# 函数注释 '->' 我的python代码是什么?
'''
你有没有看到任何Python代码在函数定义的parantheses中使用冒号？
'''
def foo1(x: 'insert x here', y: 'insert x^2 here'):
    print('Hello, World')
    return
def foo2(x, y) -> 'Hi!':
    print('Hello, World')
    return
'''
问：这是有效的Python语法吗？
A：是的

问：那么如果我刚刚调用函数会怎么样？
A：没什么！

这是证明！
'''
foo1(1, 2)
foo2(1, 2)
print(foo1.__annotations__)
print(foo2.__annotations__)
'''
**所以，那些是函数注释... **

冒号的功能参数
返回值的箭头
你可能永远不会使用它们（或至少很少）。通常，我们在函数下面写一个很好的函数文档作为一个docstring - 或至少这是我该怎么做
'''

