#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

#list
#list是一种有序的集合，可以随时添加和删除其中的元素
classmates = ['afa', 'axing','ahua'];
print(classmates,',', len(classmates),',', classmates[0], classmates[1], classmates[2])
print(classmates[-1], classmates[-2], classmates[-3])
classmates.append('Adam')
print(classmates)
classmates.pop()
print(classmates)

#要删除指定位置的元素,'.pop()'默认删除最后一个元素并返回删除的值
classmates.pop(1)
print(classmates)

#从 list 中删除元素
'''
(1) remove 从 list 中删除一个值的首次出现。
(2) remove 仅仅 删除一个值的首次出现。在这里, 'new' 在 list 中出现了两次,
但 li.remove("new") 只删除了 'new' 的首次出现。
(3) 如果在 list 中没有找到值,Python 会引发一个异常来响应 index 方法。
(4) pop 是一个有趣的东西。它会做两件事:删除 list 的最后一个元素,然后
返回删除元素的值。请注意,这与 li[-1] 不同,后者返回一个值但不改变
list 本身。也不同于 li.remove(value) ,后者改变 list 但并不返回值
'''
li = ['a', 'b', 'new', 'mpilgrim', 'z', 'example', 'new', 'two', 'elements']
li.remove('z')
print(li)
li.remove('new')
print(li)
li.pop()
print(li)

#List 运算符
'''
(1) Lists 也可以用 + 运算符连接起来。 list = list + otherlist 相当于list.extend(otherlist) 。但 + 运算符把一个新 (连接后) 的 list 作为值返回,而
extend只修改存在的 list。也就是说,对于大型 list 来说, extend 的执行速度要快一些。
(2) Python 支持 += 运算符。 li += ['two'] 等同于 li.extend(['two']) 。 += 运算符可用于
list、字符串和整数,并且它也可以被重载用于用户自定义的类中 (更多关于类的内容参见 第 5 章 )。
(3) * 运算符可以作为一个重复器作用于 list。 li = [1, 2] * 3 等同于 li = [1, 2] + [1,
2] + [1, 2] ,即将三个list 连接成一个。
'''
li = ['a', 'b', 'mpilgrim']
print(li)
li = li + ['example', 'new']
print(li)
li += ['two']
print(li)

li = [1,2] * 3
print(li)


#把某个元素替换成别的元素，可以直接赋值给对应的索引位置
classmates[1] = 'amei'
print(classmates)

#list里面的元素的数据类型也可以不同
L = ['Apple', 123, True]
print(L)

#list元素也可以是另一个list
s = ['python', 'java', ['asp', 'php'], 'scheme']
print(len(s), ',', s)

#tuple有序列表叫元组
#tuple和list非常类似，但是tuple一旦初始化就不能修改
#Tuple 没有方 法
classmates = ('Michael', 'Bob', 'Tracy')
print(classmates)

#要定义一个只有1个元素的tuple
#只有1个元素的tuple定义时必须加一个逗号,来消除歧义
t = (1,)
print(t)

#最后来看一个“可变的”tuple
#表面上看，tuple的元素确实变了，但其实变的不是tuple的元素，而是list的元素。
#tuple一开始指向的list并没有改成别的list，所以，tuple所谓的“不变”是说，tuple的每个元素，指向永远不变。
#即指向'a'，就不能改成指向'b'，指向一个list，就不能改成指向其他对象，但指向的这个list本身是可变的！
#理解了“指向不变”后，要创建一个内容也不变的tuple怎么做？
#那就必须保证tuple的每一个元素本身也不能变。
t = ('a', 'b', ['A', 'B'])
t[2][0] = 'X'
t[2][1] = 'Y'
print(t)

#Tuple 没有方 法
'''
(1) 您不能向 tuple 增加元素。Tuple 没有 append 或 extend 方法。
(2) 您不能从 tuple 删除元素。Tuple 没有 remove 或 pop 方法。
(3) 您不能在 tuple 中查找元素。Tuple 没有 index 方法。
(4) 然而,您可以使用 in 来查看一个元素是否存在于 tuple 中
'''

#Tuple 到 list 再到 tuple
'''
Tuple 可以转换成 list,反之亦然。内置的 tuple 函数接收一个 list,并返回一
个有着相同元素的 tuple。而 list 函数接收一个 tuple 返回一个 list。从效果上
看, tuple 冻结一个 list,而 list 解冻一个 tuple。
'''

#使用 tuple 有什么好处:
'''
•
Tuple 比 list 操作速度快。如果您定义了一个值的常量集,并且唯一要用它做的是不断地遍历它,请使用 tuple 代替 list。
•
如果对不需要修改的数据进行 “写保护”,可以使代码更安全。使用tuple 而不是 list 如同拥有一个隐含的 assert 语句,说明这一数据是常量。如果必须要改变这些值,则需要执行 tuple 到 list 的转换 (需要使用一个特殊的函数)。
•
还记得我说过 dictionary keys 可以是字符串,整数和 “其它几种类型”吗?
Tuples 就是这些类型之一。Tuples 可以在 dictionary 中被用做 key,但
是 list 不行。实际上,事情要比这更复杂。Dictionary key 必须是不可变
的。Tuple 本身是不可改变的,但是如果您有一个 list 的 tuple,那就认
为是可变的了,用做 dictionary key 就是不安全的。只有字符串、整数
或其它对 dictionary 安全的 tuple 才可以用作 dictionary key。
•
Tuples 可以用在字符串格式化中,我们会很快看到
'''