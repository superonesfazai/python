#coding:utf-8

#列表解析中的第一个表达式可以是任何表达式,包括列表解析

#下面是一个3×4的矩阵
matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12]
]

#现在如果你想交换行和列,可以用嵌套的列表推导式
transposed = [[row[i] for row in matrix] for i in range(4)]
print(transposed)

#嵌套的列表推导式是对 for 后面的内容进行求值,所以上例就等价于
transposed = []
for i in range(4):
    transposed.append([row[i] for row in matrix])

print(transposed)

#在实际中,你应该更喜欢使用内置函数组成复杂流程语句,对此种情况 zip() 函数将会做的更好
transposed = list(zip(*matrix))
print(transposed)