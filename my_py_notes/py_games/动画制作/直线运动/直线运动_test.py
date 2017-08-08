# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-27 下午9:21
# @File    : 直线运动_test.py

import pygame
from pygame.locals import *
from sys import exit

pygame.init()

screen = pygame.display.set_mode((640, 480), 0, 32)

bg = pygame.image.load('../images/sushiplate.jpg')
sprite = pygame.image.load('../images/fugu.png')

# sprite的起始位置
x = 0.

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    screen.blit(bg, (0, 0))
    screen.blit(sprite, (x, 100))
    x += 5.    # 如果你的机器性能太好以至于看不清,可以把数字改小一点

    # 如果移出屏幕, 就搬到开始的位置
    if x > 640:
        x = 0.

    pygame.display.update()
