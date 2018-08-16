# coding:utf-8

'''
@author = super_fazai
@File    : scipy_base.py
@Time    : 2017/3/15 17:53
@connect : superonesfazai@gmail.com
'''

"""
NumPy替我们搞定了向量和矩阵的相关操作，基本上算是一个高级的科学计算器。
SciPy基于NumPy提供了更为丰富和高级的功能扩展，在统计、优化、插值、数值积分、时频转换等方面提供了大量的可用函数，基本覆盖了基础科学计算相关的问题

    在量化分析中，运用最广泛的是统计和优化的相关技术
"""

import numpy as np
import scipy.stats as stats
import scipy.optimize as opt

"""
统计部分
"""

# rv_continuous表示连续型的随机分布，如均匀分布（uniform）、正态分布（norm）、贝塔分布（beta）等
# rv_discrete表示离散型的随机分布，如伯努利分布（bernoulli）、几何分布（geom）、泊松分布（poisson）等

# 生成10个[0, 1]区间上的随机数
rv_unif = stats.uniform.rvs(size=10)
print(rv_unif)
# [0.40724459 0.09985714 0.81497799 0.72176607 0.13320602 0.4141679
#  0.32257506 0.67493034 0.02521065 0.59899874]

# 生成10个服从参数a=4，b=2的贝塔分布随机数
rv_beta = stats.beta.rvs(size=10, a=4, b=2)
print(rv_beta)
# [0.82845095 0.61869186 0.48966922 0.82297325 0.57183903 0.54696049
#  0.53687095 0.15694508 0.68522656 0.61492356]

"""
优化部分
"""




