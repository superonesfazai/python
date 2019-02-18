# coding:utf-8

'''
@author = super_fazai
@File    : 定义list类型的别名.py
@connect : superonesfazai@gmail.com
'''

from typing import List

# 类型注释可让你的代码更容易被理解，他们还允许在运行前使用类型检查来捕获这些杂散的类型错误，在大型项目中更值得使用!
Vector = List[float]
Matrix = List[Vector]

def add_matrix(a: Matrix, b: Matrix) -> Matrix:
    res = []
    for i, row in enumerate(a):
        res_row = []
        for j, col in enumerate(row):
            res_row = [a[i][j] + b[i][j]]

        res += [res_row]

    return res

x = [
    [1.0, 0.],
    [0., 1.01],
]
y = [
    [2.0, 1.0],
    [0., -2.]
]
z = add_matrix(x, y)
print(z)