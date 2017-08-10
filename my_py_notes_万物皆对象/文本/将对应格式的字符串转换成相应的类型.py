# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-24 上午9:42
# @File    : 将对应格式的字符串转换成相应的类型.py

# eval内建函数
a = [1, 2, 3]
b = str(a)
print(b)
result = eval(b)
print(result)

c = '{1:\'a\', 2:\'b\'}'
print(eval(c))

def pr():
    print('*' * 20)

w = pr()
print(eval(str(w)))

def f_read_test():
    with open('1', 'r') as f:
        for line in f:
            print(line, end='')

print(eval(str(f_read_test())))
