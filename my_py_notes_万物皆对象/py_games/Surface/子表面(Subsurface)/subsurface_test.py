# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-27 下午6:48
# @File    : subsurface_test.py

'''
Subsurface就是在一个Surface中再提取一个Surface
记住当你往Subsurface上画东西的时候,同时也向父表面上操作
这可以用来绘制图形文字,尽管pygame.font可以用来写很不错的字
但只是单色, 游戏可能需要更丰富的表现,这时候你可以把每个字母(中文的话有些吃力了)
各自做成一个图片,不过更好的方法是在一张图片上画满所有的字母.
把整张图读入,然后再用Subsurface把字母一个一个'抠'出来,就像下面这样
'''

import pygame
from pygame.locals import *

my_font_image = pygame.image.load("font.png")
letters = []
letters["a"] = my_font_image.subsurface((0,0), (80,80))
letters["b"] = my_font_image.subsurface((80,0), (80,80))