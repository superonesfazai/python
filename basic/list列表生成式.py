#!/usr/bin/python3.5
# -*- coding:utf-8 -*-

#列表生成式
#列表生成式即List Comprehensions，是Python内置的非常简单却强大的可以用来创建list的生成式
print(list(range(1, 11)))
#如果要生成[1x1, 2x2, 3x3, ..., 10x10]怎么做？
print([x * x for x in range(1, 11)])
#写列表生成式时，把要生成的元素x * x放到前面，后面跟for循环，就可以把list创建出来，十分有用，多写几次，很快就可以熟悉这种语法
#for循环后面还可以加上if判断，这样我们就可以筛选出仅偶数的平方
print([x * x for x in range(1, 11) if x % 2 == 0])
#还可以使用两层循环，可以生成全排列
print([m + n for m in 'ABC' for n in 'XYZ'])
#三层和三层以上的循环就很少用到了
#运用列表生成式，可以写出非常简洁的代码。
#例如，列出当前目录下的所有文件和目录名，可以通过一行代码实现
import os #导入os模块
print([d for d in os.listdir('.')]) #os.listdir可以列出文件和目录

#for循环其实可以同时使用两个甚至多个变量
#比如dict的items()可以同时迭代key和value
#d = {'x': 'A', 'y': 'B', 'z': 'C'}

d = {'x': 'a', 'y': 33}
for k, v in d.items():
    print(k, '=', v)

#因此，列表生成式也可以使用两个变量来生成list
print([k + '=' + v for k, v in d.items() if isinstance(v, str)])

#最后把一个list中所有的字符串变成小写
L = ['Hello', 'World', 'IBM', 'Apple']
print([s.lower() for s in L])

#如果list中既包含字符串，又包含整数，由于非字符串类型没有lower()方法，所以列表生成式会报错
#使用内建的isinstance函数可以判断一个变量是不是字符串
#通过添加if语句保证列表生成式能正确地执行
x = 'abc'
y = 123
print(isinstance(x, str))
print(isinstance(y, str))
