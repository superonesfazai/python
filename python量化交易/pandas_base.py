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

"""
操作pandas数据
"""
# 为了看数据方便，可以设置输出屏幕的宽度
print('-' * 100)
pd.set_option('display.width', 200)

'''数据创建的其他方式'''

# 创建一个以日期为元素的Series
dates = pd.date_range('20150101', periods=5)
print(dates)    # DatetimeIndex(['2015-01-01', '2015-01-02', '2015-01-03', '2015-01-04', '2015-01-05'], dtype='datetime64[ns]', freq='D')

# 将这个日期Series作为索引赋给一个DataFrame
df = pd.DataFrame(np.random.randn(5, 4),index=dates,columns=list('ABCD'))
print(df)
#                    A         B         C         D
# 2015-01-01  0.204720 -0.201529 -0.019477 -1.849065
# 2015-01-02 -0.580994  1.022587  0.243434 -0.557614
# 2015-01-03  0.835094  0.672479 -0.426564  0.031152
# 2015-01-04 -2.244592  1.248810 -0.468399 -0.219757
# 2015-01-05  0.266533  0.376372 -0.339831  0.720766

# 只要是能转换成Series的对象，都可以用于创建DataFrame
df2 = pd.DataFrame({ 'A' : 1., 'B': pd.Timestamp('20150214'), 'C': pd.Series(1.6,index=list(range(4)),dtype='float64'), 'D' : np.array([4] * 4, dtype='int64'), 'E' : 'hello pandas!' })
print(df2)
#      A          B    C  D              E
# 0  1.0 2015-02-14  1.6  4  hello pandas!
# 1  1.0 2015-02-14  1.6  4  hello pandas!
# 2  1.0 2015-02-14  1.6  4  hello pandas!
# 3  1.0 2015-02-14  1.6  4  hello pandas!

"""
数据的查看
"""
print(df.head())
print(df.tail(3))
#                    A         B         C         D
# 2015-01-01  1.152769  1.792713  0.798349 -0.322211
# 2015-01-02  0.426192 -0.181601 -0.627751  1.546968
# 2015-01-03 -0.972046  0.966826 -0.057681  1.208090
# 2015-01-04 -1.679944  0.494935 -0.794716 -1.325956
# 2015-01-05  1.479955  0.347468  0.273907 -1.475466
#                    A         B         C         D
# 2015-01-03 -0.972046  0.966826 -0.057681  1.208090
# 2015-01-04 -1.679944  0.494935 -0.794716 -1.325956
# 2015-01-05  1.479955  0.347468  0.273907 -1.475466

print(df.describe())
#               A         B         C         D
# count  5.000000  5.000000  5.000000  5.000000
# mean   0.346135 -0.961701  0.751650  0.352537
# std    0.768513  0.664497  0.286788  0.979257
# min   -0.478170 -1.797218  0.519188 -0.644772
# 25%   -0.142785 -1.364953  0.601897 -0.546824
# 50%    0.183255 -0.901644  0.694344  0.296851
# 75%    0.679243 -0.694238  0.695142  1.080373
# max    1.489130 -0.050449  1.247681  1.577059

# 数据排序
# DataFrame提供了两种形式的排序。
# 一种是按行列排序，即按照索引（行名）或者列名进行排序，可调用dataframe.sort_index，指定axis=0表示按索引（行名）排序，axis=1表示按列名排序，并可指定升序或者降序
print(df.sort_index(axis=1, ascending=False).head())
#                    D         C         B         A
# 2015-01-01  0.618740  0.650590  0.052638  1.334794
# 2015-01-02  0.340570 -0.906048  0.404482 -1.648764
# 2015-01-03  0.804632 -0.737653  0.055764 -0.334571
# 2015-01-04 -0.589778 -0.094570 -0.587296 -0.763648
# 2015-01-05  0.044815 -1.261772 -1.524638 -1.497966

# 第二种排序是按值排序，可指定列名和排序方式，默认的是升序排序
# eg:
# print(df.sort(columns='tradeDate').head())
# df = df.sort(columns=['tradeDate', 'secID'], ascending=[False, True])
# print(df.head())

'''再谈数据访问'''
print(df.iloc[1:4][:])
#                    A         B         C         D
# 2015-01-02  2.192268 -0.090566  0.392206  2.096466
# 2015-01-03  0.785864  0.123506 -0.886260 -0.963253
# 2015-01-04 -1.022874 -2.103927 -0.667007 -1.709404

# ** isin()函数可方便地过滤DataFrame中的数据

'''处理缺失数据'''
# 让其 = np.nan

# 处理缺失数据有多种方式。通常使用dataframe.dropna()，dataframe.dropna()可以按行丢弃带有nan的数据；
# 若指定how='all'（默认是'any'），则只在整行全部是nan时丢弃数据；若指定thresh，则表示当某行数据非缺失列数超过指定数值时才保留；
# 要指定根据某列丢弃可以通过subset完成

# 此外: 有数据缺失时也未必是全部丢弃，dataframe.fillna(value=value)可以指定填补缺失值的数值

"""
数据操作
"""
# Series和DataFrame的类函数提供了一些函数，如mean()、sum()等
# value_counts函数可以方便地统计频数

# 在panda中，Series可以调用map函数来对每个元素应用一个函数，DataFrame可以调用apply函数对每一列（行）应用一个函数，applymap对每个元素应用一个函数。
# 这里面的函数可以是用户自定义的一个lambda函数，也可以是已有的其他函数。下例展示了将收盘价调整到[0, 1]区间
# eg:
# print(df[['closePrice']].apply(lambda x: (x - x.min()) / (x.max() - x.min())).head())

# 使用append可以在Series后添加元素，以及在DataFrame尾部添加一行

# ** DataFrame另一个强大的函数是groupby，可以十分方便地对数据分组处理

"""
数据可视化
"""


