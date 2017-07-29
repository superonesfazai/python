# coding: utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-20 下午9:08
# @File    : test.py

# 计算1!+2!+3!...+20! =
tmp = []

def fact():
    global tmp
    for i in range(1, 10):
        s = 1
        for j in range(1, i+1):
            s = s * j
            print('ss=', s)
        tmp.append(s)
    return tmp

sum = 0
fact()
for i in range(0, len(tmp)):
    sum = sum + int(tmp[i])

print(sum)

for i in range(3):
    print(i)

a = {'a': 1, '2': 2}

# 以dict传参
def t(**kwargs):
    for k, v in kwargs.items():
        print(k, '=', v)

t(**a)



