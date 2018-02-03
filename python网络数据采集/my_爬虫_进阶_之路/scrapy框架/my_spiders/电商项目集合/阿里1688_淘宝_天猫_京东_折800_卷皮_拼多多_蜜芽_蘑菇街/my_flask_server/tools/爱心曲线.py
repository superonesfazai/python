# coding:utf-8

'''
@author = super_fazai
@File    : 爱心曲线.py
@Time    : 2018/2/3 15:37
@connect : superonesfazai@gmail.com
'''

# 爱心曲线一

# import numpy as np
# import matplotlib.pyplot as plt
# a = 1
# t = np.linspace(0 , 2 * np.pi, 1024)
# X = a*(2*np.cos(t)-np.cos(2*t))
# Y = a*(2*np.sin(t)-np.sin(2*t))
# plt.plot(Y, X,color='r')
# plt.show()

# 爱心曲线二
import numpy as np
import matplotlib.pyplot as plt
T = np.linspace(0 , 2 * np.pi, 1024)
plt.axes(polar = True)
plt.plot(T, 1. - np.sin(T),color="r")
plt.show()