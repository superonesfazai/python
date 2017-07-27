# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-27 下午12:15
# @File    : 显示中文_test.py

import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)

# font = pygame.font.SysFont("宋体", 40)
# font = pygame.font.SysFont("simsunnsimsun", 40)
# 用get_fonts()查看后看到了这个字体名，在我的机器上可以正常显示了
font = pygame.font.Font("simsun.ttf", 40)
# 这句话总是可以的，所以还是TTF文件保险啊
text_surface = font.render(u"你好", True, (0, 0, 255))

x = 0
y = (480 - text_surface.get_height()) / 2

background = pygame.image.load("../images/sushiplate.jpg")

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    screen.blit(background, (0, 0))

    x -= 2  # 文字滚动太快的话，改改这个数字
    if x < -text_surface.get_width():
        x = 640 - text_surface.get_width()

    screen.blit(text_surface, (x, y))

    pygame.display.update()