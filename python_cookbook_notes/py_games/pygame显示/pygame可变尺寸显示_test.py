# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-27 上午11:16
# @File    : pygame可变尺寸显示_test.py

import pygame
from pygame.locals import *
from sys import exit

SCREEN_SIZE = (640, 480)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)

background = pygame.image.load('../images/sushiplate.jpg')

while True:
    event = pygame.event.wait()
    if event.type == QUIT:
        exit()
    if event.type == VIDEORESIZE:
        SCREEN_SIZE = event.size
        screen = pygame.display.set_mode(SCREEN_SIZE, RESIZABLE, 32)
        pygame.display.set_caption('Window resized to ' + str(event.size))

    screen_width, screen_height = SCREEN_SIZE
    # 这里需要重新填满窗口
    for y in range(0, screen_height, background.get_height()):
        for x in range(0, screen_width, background.get_width()):
            screen.blit(background, (x, y))

    pygame.display.update()

'''
当你更改大小的时候,后端控制台会显示出新的尺寸
这里我们学习到一个新的事件VIDEORESIZE,它包含如下内容：
    size  —  一个二维元组，值为更改后的窗口尺寸，size[0]为宽，size[1]为高
    w  —  宽
    h  —  一目了然，高；之所以多出这两个，无非是为了方便
'''