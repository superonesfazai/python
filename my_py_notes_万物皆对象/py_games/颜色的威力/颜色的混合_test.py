# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-27 下午12:43
# @File    : 颜色的混合_test.py

'''
很多时候我们还需要混合颜色,
比如一个僵尸在路过一个火山熔岩坑的时候,
它会由绿色变成橙红色,
再变为正常的绿色,
这个过程必须表现的很平滑,
这时候我们就需要混合颜色
'''

# 我们用一种叫做'线性插值(linear interpolation)'的方法来做这件事情
# 为了找到两种颜色的中间色,我们将这第二种颜色与第一种颜色的差乘以一个0~1之间的小数
# 然后再加上第一种颜色就行了
# 如果这个数为0,结果就完全是第一种颜色; 是1,结果就只剩下第二种颜色; 中间的小数则会皆有两者的特色

#!/usr/bin/env python

import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)

color1 = (221, 99, 20)
color2 = (96, 130, 51)
factor = 0.

def blend_color(color1, color2, blend_factor):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    r = r1 + (r2 - r1) * blend_factor
    g = g1 + (g2 - g1) * blend_factor
    b = b1 + (b2 - b1) * blend_factor
    return int(r), int(g), int(b)

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    screen.fill((255,255,255))

    tri = [ (0, 120), (639, 100), (639, 140) ]
    pygame.draw.polygon(screen, (0, 255, 0), tri)
    pygame.draw.circle(screen, (0, 0, 0), (int(factor * 639.0), 120), 10)

    x, y = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        factor = x / 639.0
        pygame.display.set_caption("Pygame Color Blend Test - %.3f" % factor)

    color = blend_color(color1, color2 , factor)
    pygame.draw.rect(screen, color, (0, 240, 640, 240))

    pygame.display.update()

# 移动小球你能看到下方的颜色在'火球橙'和'僵尸绿'之间渐变
# 更改代码里的color1和color2. 你能看到任意两种颜色渐变的过程！