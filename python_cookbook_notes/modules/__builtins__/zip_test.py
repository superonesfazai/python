# coding = utf-8

'''
@author = super_fazai
@File    : zip_test.py
@Time    : 2017/8/4 18:07
@connect : superonesfazai@gmail.com
'''

s, t = 'asd', 'zxc'
print(list(zip(s, t)))

tmp = ([1, 2, 3],
       [4, 5, 6],
       [7, 8, 9])
tmp2 = ([3, 2, 1],
        [6, 5, 4],
        [9, 8, 7])
print(list(zip(tmp, tmp2)))