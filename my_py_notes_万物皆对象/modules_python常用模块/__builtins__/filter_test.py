# coding = utf-8

'''
@author = super_fazai
@File    : filter_test.py
@Time    : 2017/8/7 15:45
@connect : superonesfazai@gmail.com
'''

'''
filter函数会对指定序列执⾏过滤操作
    filter(function or None, iterable) --> filter object
        Return an iterator yielding those items of iterable for which function(item) is true. If function is None, return the items that are true.
        function:接受⼀个参数， 返回布尔值True或False
        iterable:序列可以是str， tuple， list
        filter函数会对序列参数iterable中的每个元素调⽤function函数
        最后返回的结果包含调⽤结果为True的元素。
        返回值的类型和参数iterable的类型相同
'''

print(list(filter(lambda x: x%2, [1, 2, 3, 4])))

print(str(filter(None, 'she')))

'''
python3测试结果:
[1, 3]
<filter object at 0x106485668>
'''