#coding: utf-8

#上三角
for i in range(1, 6):
    for j in range(i):
        print('*', end=' ')
    print()

print()

#下三角
tmp_num = 5
while tmp_num <= 5 and tmp_num >=0:
    for j in range(tmp_num):
        print('*', end=' ')
    tmp_num -= 1
    print()

# 上下三角
num = int(input('请输入要打印上三角的行数：'))
for i in range(1, num+1):
    for j in range(i):
        print('*', end=' ')
    print()
tmp_num = num - 1
while tmp_num <= num and tmp_num >=0:
    for j in range(tmp_num):
        print('*', end=' ')
    tmp_num -= 1
    print()

print()

#9x9
for i in range(1, 10):
    for j in range(1, i+1):
        print('%d*%d=%d ' % (j, i, j*i), end='')
    print()

print()
#
i=1
while i <= 9:
    if i <= 5:
        print(' '*(5-i),'*'*(2*i-1))
    else:
        print(' '*(i-5), '*'*(2*(10-i)-1))
    i+=1

#