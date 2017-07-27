# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-27 上午9:05
# @File    : hello_world.py

import pygame
from pygame.locals import *     # 导入常用函数和变量
from sys import exit            # 借个模块用于退出程序

pygame.init()       # 初始化pygame,为硬件做准备

screen = pygame.display.set_mode((640, 480), 0, 32)     # 创建一个窗口
pygame.display.set_caption('hello, world!')     # 设置窗口标题

# 加载并转换图像
bground = pygame.image.load('images/sushiplate.jpg')
mouse_cursor = pygame.image.load('images/fugu.png')

while True:     # 游戏主循环
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    screen.blit(bground, (0, 0))        # 将背景图画上去

    x, y = pygame.mouse.get_pos()       # 获取鼠标位置

    x -= mouse_cursor.get_width()/2     # 计算光标的左上角位置
    y -+ mouse_cursor.get_height()/2

    screen.blit(mouse_cursor, (x, y))   # 把光标画上去

    pygame.display.update()             # 刷新界面

'''
convert函数是将图像数据都转化为Surface对象
每次加载完图像以后就应该做这件事件(事实上因为 它太常用了
如果你不写pygame也会帮你做);convert_alpha相比convert
保留了Alpha 通道信息（可以简单理解为透明的部分),这样我们的光标才可以是不规则的形状
'''