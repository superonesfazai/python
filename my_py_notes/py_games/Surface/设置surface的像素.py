# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-27 下午6:53
# @File    : 设置surface的像素.py
'''
我们能对Surface做的最基本的操作就是设置一个像素的色彩了
虽然我们基本不会这么做,但还是要了解
set_at方法可以做到这一点,它的参数是坐标和颜色
下面的小脚本会随机的在屏幕上画点
'''

import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)

full_screen = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    rand_col = (randint(0, 255), randint(0, 255), randint(0, 255))
    #screen.lock()    #很快你就会知道这两句lock和unlock的意思了
    for _ in range(100):
        rand_pos = (randint(0, 639), randint(0, 479))
        screen.set_at(rand_pos, rand_col)
    #screen.unlock()

    pygame.display.update()