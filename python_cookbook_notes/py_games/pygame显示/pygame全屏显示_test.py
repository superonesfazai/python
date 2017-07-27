# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-27 上午10:54
# @File    : pygame全屏显示_test.py

# import pygame
# from pygame.locals import *
#
# pygame.init()
#
# # 全屏显示
# screen = pygame.display.set_mode((640, 480), 0, 32)
# screen = pygame.display.set_mode((640, 480), FULLSCREEN, 32)

# 在全屏模式下,显卡可能就切换了一种模式
# 你可以用如下代码获得您的机器支持的显示模式：
# >>> import pygame
# >>> pygame.init()
# >>> pygame.display.list_modes()

# 运行这个程序,默认还是窗口的，按'f',显示模式会在窗口和全屏之间切换
import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
background = pygame.image.load('../images/sushiplate.jpg')

Fullscreen = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    if event.type == KEYDOWN:
        if event.key == K_f:
            Fullscreen = not Fullscreen
            if Fullscreen:
                screen = pygame.display.set_mode((640, 480), FULLSCREEN, 32)
            else:
                screen = pygame.display.set_mode((640, 480), 0, 32)

    screen.blit(background, (0, 0))
    pygame.display.update()