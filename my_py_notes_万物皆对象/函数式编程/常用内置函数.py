# coding:utf-8

'''
@author = super_fazai
@File    : 常用内置函数.py
@connect : superonesfazai@gmail.com
'''

# filter函数
# 功能相当于过滤器。调用一个布尔函数bool_func来迭代遍历每个seq中的元素；返回一个使bool_seq返回值为true的元素的序列。
a = [
    {
        'id': 1,
    },{
        'id': 2,
    }
]

b = filter(lambda x: x.get('id') > 1, a)
print(list(b))

# map函数
# 是对一个序列的每个项依次执行函数
a = map(lambda x:x*2,[1,2,3])
print(list(a))