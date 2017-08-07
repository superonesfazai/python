# coding = utf-8

'''
@author = super_fazai
@File    : map_test.py
@Time    : 2017/8/7 15:34
@connect : superonesfazai@gmail.com
'''
'''
map函数会根据提供的函数对指定序列做映射
    map(function, *iterables) -> list   # python2中直接返回list
                                        # python3中还得用list进行类型转换
        function:是⼀个函数
        *iterables:是⼀个或多个序列,取决于function需要⼏个参数
        参数序列中的每⼀个元素分别调⽤function函数, 返回包含每次function函数返回值的list。
'''

# 函数需要1个参数时
print(list(map(lambda x: x*x, [1, 2, 3])))

# 函数需要2个参数时
print(list(map(lambda x, y: x+y, [1, 2, 3], [4, 5, 6])))

def f1(x, y):
    return (x, y)

l1 = [ 0, 1, 2, 3, 4, 5, 6 ]
l2 = [ 'Sun', 'M', 'T', 'W', 'T', 'F', 'S' ]
l3 = map(f1, l1, l2)
print(list(l3))

'''
测试结果:
[1, 4, 9]
[5, 7, 9]
[(0, 'Sun'), (1, 'M'), (2, 'T'), (3, 'W'), (4, 'T'), (5, 'F'), (6, 'S')]
'''