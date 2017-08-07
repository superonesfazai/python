# coding = utf-8

'''
@author = super_fazai
@File    : reduce_test.py
@Time    : 2017/8/7 15:58
@connect : superonesfazai@gmail.com
'''

'''
reduce函数会对参数序列中元素进⾏累积
    reduce(function, sequence[, initial]) -> value
        Apply a function of two arguments cumulatively to the items of a sequence,
        from left to right, so as to reduce the sequence to a single value.
        For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) 
        calculates ((((1+2)+3)+4)+5).  
        If initial is present, it is placed before the items of the sequence in the calculation, 
        and serves as a default when the sequence is empty.
        
        function:该函数有两个参数
        sequence:序列可以是str， tuple， list
        initial:固定初始值
'''
# import functools
from functools import reduce

print(reduce(lambda x, y: x+y, [1, 2, 3, 4]))

print(reduce(lambda x, y: x+y, [1, 2, 3, 4], 5))

print(reduce(lambda x, y: x+y, ['aa', 'bb', 'cc', 'dd'], 'ee'))

'''
reduce依次从sequence中取⼀个元素, 和上⼀次调⽤function的结果做参数
再次调⽤function. 第⼀次调⽤function时, 如果提供initial参数, 
会以sequence中的第⼀个元素和initial 作为参数调⽤function, 
否则会以序列sequence中的前两个元素做参数调⽤function. 
注意function函数不能为None
'''

'''
在Python3⾥,reduce函数已经被从全局名字空间⾥移除了, 它现在被放
置在fucntools模块⾥⽤的话要先引⼊： from functools import
reduce
'''

'''
测试结果:
10
15
eeaabbccdd
'''