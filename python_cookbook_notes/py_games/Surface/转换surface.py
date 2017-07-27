# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-27 下午6:10
# @File    : 转换surface.py

import pygame
'''
通常你不用在意surface里的具体内容
不过也许需要把这些surface转换一下以获得更高的性能
还记得一开始的程序中的两句话吗：
'''

background = pygame.image.load('../images/sushiplate.jpg').convert()
mouse_cursor = pygame.image.load('../images/fugu.png').convert_alpha()

'''
第一句是普通的转换,相同于display；
第二句是带alpha通道的转换
如果你给convert或者conver_alpha一个surface对象作为参数
那么这个会被作为目标来转换
'''