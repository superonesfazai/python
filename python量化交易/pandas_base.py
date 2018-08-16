# coding:utf-8

'''
@author = super_fazai
@File    : pandas_base.py
@Time    : 2017/3/16 11:29
@connect : superonesfazai@gmail.com
'''

"""
pandas包含了高级的数据结构Series和DataFrame，使得在Python中处理数据变得非常方便、快速和简单
"""

import numpy as np
from pandas import Series, DataFrame
import pandas as pd

"""
pandas数据结构: Series
"""
# 从一般意义上来讲，Series可以简单地被认为是一维的数组。
# Series和一维数组最主要的区别在于Series类型具有索引（index），可以和另一个编程中常见的数据结构哈希（Hash）联系起来

'''创建Series'''
a = np.random.randn(5)
print(a)        # [ 0.65744567  0.73483442  0.79069926  0.0381571  -0.84003597]
s = Series(a)
print(s)
# 0    0.657446
# 1    0.734834
# 2    0.790699
# 3    0.038157
# 4   -0.840036
# dtype: float64

# 可以在创建Series时添加index，并可使用Series.index查看具体的index
# 需要注意的一点是，当从数组创建Series时，若指定index，那么index长度要和data的长度一致
s = Series(np.random.randn(5), index=['a', 'b', 'c', 'd', 'e'])
print(s)
# a    0.584242
# b    0.046837
# c    0.815198
# d    0.066705
# e    0.563855
# dtype: float64
print(s.index)      # Index(['a', 'b', 'c', 'd', 'e'], dtype='object')

# 创建Series的另一个可选项是name，可指定Series的名称，可用Series.name访问
# 在随后的DataFrame中，每一列的列名在该列被单独取出来时就成了Series的名称
s = Series(np.random.randn(5), index=['a', 'b', 'c', 'd', 'e'], name='my_series')
print(s)
# a   -0.446331
# b   -0.396748
# c    1.223288
# d    0.429643
# e   -0.914034
# Name: my_series, dtype: float6
print(s.name)       # my_series

# Series还可以从字典（dict）创建
d = {'a': 0., 'b': 1, 'c': 2}
s = Series(d)
print(s)
# a    0.0
# b    1.0
# c    2.0
# dtype: float64

# 让我们来看看使用字典创建Series时指定index的情形（index长度不必和字典相同）
s = Series(d, index=['b', 'c', 'd', 'a'])
print(s)
# b    1.0
# c    2.0
# d    NaN
# a    0.0
# dtype: float64

# 如果数据就是一个单一的变量，如数字
s = Series(4., index=['a', 'b', 'c', 'd', 'e'])
print(s)
# a    4.0
# b    4.0
# c    4.0
# d    4.0
# e    4.0
# dtype: float64

'''Series的数据访问'''
s = Series(np.random.randn(10),index=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])
print(s[0])
print(s[:2])
# a   -0.809849
# b    1.420910
# dtype: float64
print(s[[2,0,4]])
# c   -0.445976
# a    0.382721
# e   -3.135186
# dtype: float64
print(s[['e', 'i']])
# e    0.041988
# i   -0.888165
# dtype: float64
print(s[s > 0.5])
# b    1.162437
# c    1.174755
# d    0.613319
# f    0.989831
# dtype: float64
print('e' in s)     # True

"""
pandas的数据结构: DataFrame
"""
# DataFrame是一个二维的数据结构，是多个Series的集合体

'''创建DataFrame'''
# 从字典创建DataFrame
d = {'one': Series([1., 2., 3.], index=['a', 'b', 'c']), 'two': Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])}
df = DataFrame(d)
print(df)
#    one  two
# a  1.0  1.0
# b  2.0  2.0
# c  3.0  3.0
# d  NaN  4.0

# 使用dataframe.index和dataframe.columns来查看DataFrame的行和列
print(df.index)     # Index(['a', 'b', 'c', 'd'], dtype='object')
print(df.columns)   # Index(['one', 'two'], dtype='object')

# dataframe.values则以数组的形式返回DataFrame的元素
print(df.values)
# [[ 1.  1.]
#  [ 2.  2.]
#  [ 3.  3.]
#  [nan  4.]]

# DataFrame也可以从值是数组的字典创建，但是各个数组的长度需要相同
d = {'one': [1., 2., 3., 4.], 'two': [4., 3., 2., 1.]}
df = DataFrame(d, index=['a', 'b', 'c', 'd'])
print(df)
#    one  two
# a  1.0  4.0
# b  2.0  3.0
# c  3.0  2.0
# d  4.0  1.0

# 值非数组时，没有这一限制，并且缺失值补成NaN
d = [{'a': 1.6, 'b': 2}, {'a': 3, 'b': 6, 'c': 9}]
df = DataFrame(d)
print(df)
# a  b    c
# 0  1.6  2  NaN
# 1  3.0  6  9.0

# 在实际处理数据时，有时需要创建一个空的DataFrame
df = DataFrame()
print(df)
# Empty DataFrame
# Columns: []
# Index: []

# ** 另一种创建DataFrame的方法十分有用，那就是使用concat函数基于Series或者DataFrame创建一个DataFrame
a = Series(range(5))
b = Series(np.linspace(4, 20, 5))
df = pd.concat([a, b], axis=1)      # 其中的axis=1表示按列进行合并，axis=0表示按行合并
print(df)
#    0     1
# 0  0   4.0
# 1  1   8.0
# 2  2  12.0
# 3  3  16.0
# 4  4  20.0

# 按行合并DataFrame成一个大的DataFrame
df = DataFrame()
index = ['alpha', 'beta', 'gamma', 'delta', 'eta']
for i in range(5):
    a = DataFrame([np.linspace(i, 5*i, 5)], index=[index[i]])
    df = pd.concat([df, a], axis=0)
print(df)
#          0    1     2     3     4
# alpha  0.0  0.0   0.0   0.0   0.0
# beta   1.0  2.0   3.0   4.0   5.0
# gamma  2.0  4.0   6.0   8.0  10.0
# delta  3.0  6.0   9.0  12.0  15.0
# eta    4.0  8.0  12.0  16.0  20.0

'''DataFrame数据的访问'''
# 再次强调一下DataFrame是以列作为操作的基础的，全部操作都想象成先从DataFrame里取一列，再从这个Series取元素即可
# 可以用datafrae.column_name选取列，也可以使用dataframe[]操作选取列
print(df[1])
# alpha    0.0
# beta     2.0
# gamma    4.0
# delta    6.0
# eta      8.0
# Name: 1, dtype: float64
print(type(df[1]))      # <class 'pandas.core.series.Series'>
df.columns = ['a', 'b', 'c', 'd', 'e']
print(df['b'])
# alpha    0.0
# beta     2.0
# gamma    4.0
# delta    6.0
# eta      8.0
# Name: b, dtype: float64
print(type(df['b']))
print(df.b)
print(type(df.b))
print(df[['a', 'd']])
#          a     d
# alpha  0.0   0.0
# beta   1.0   4.0
# gamma  2.0   8.0
# delta  3.0  12.0
print(type(df[['a', 'd']]))     # <class 'pandas.core.frame.DataFrame'>

# 若需要选取行，可以使用dataframe.iloc按下标选取，或者使用dataframe.loc按索引选取
print(df.iloc[1])
# a    1.0
# b    2.0
# c    3.0
# d    4.0
# e    5.0
# Name: beta, dtype: float64
print(df.loc['beta'])
# a    1.0
# b    2.0
# c    3.0
# d    4.0
# e    5.0
# Name: beta, dtype: float64

# 切片
print(df[1:3])
#          a    b    c    d     e
# beta   1.0  2.0  3.0  4.0   5.0
# gamma  2.0  4.0  6.0  8.0  10.0

# 如果不是需要访问特定行列，而只是某个特殊位置的元素的话
# dataframe.at和dataframe.iat是最快的方式，它们分别用于使用索引和下标进行访问
print(df.iat[2, 3])         # 8.0
print(df.at['gamma', 'd'])  # 8.0

# dataframe.ix可以混合使用索引和下标进行访问
# 唯一需要注意的地方是行列内部需要一致，不可以同时使用索引和标签访问行或者列，不然的话，将会得到意外的结果
print(df.ix['gamma', 4])
print(df.ix[['delta', 'gamma'], [1, 4]])
print(df.ix[[1, 2], ['b', 'e']])
# print("Unwanted result:")
# print(df.ix[['beta', 2], ['b', 'e']])
# print(df.ix[[1, 2], ['b', 4]])
