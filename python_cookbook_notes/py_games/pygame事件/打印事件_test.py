# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-27 上午9:42
# @File    : 打印事件_test.py

import pygame
from pygame.locals import *
from sys import exit

pygame.init()
SCREEN_SIZE = (640, 480)
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

font = pygame.font.SysFont('arial', 16)
font_height = font.get_linesize()
event_text = []

while True:
    event = pygame.event.wait()
    # 获取事件名称
    event_text.append(str(event))
    # 这个切片操作保证了event_text里面只保留一个屏幕的文字
    event_text = event_text[-(SCREEN_SIZE[1]/font_height):]

    if event.type == QUIT:
        exit()

    screen.fill((255, 255, 255))

    # 找一个合适的起笔位置,最下面开始但是要留一行的空
    for text in reversed(event_text):
        screen.blit(font.render(text, True, (0, 0, 0)), (0, y))
        # 把笔提一行
        y -= font_height

    pygame.display.update()

'''
这个程序在你移动鼠标的时候产生了海量的信息
让我们知道了Pygame是多么的繁忙……
我之前是调用pygame.mouse.get_pos()来得到当前鼠标的位置
而现在利用事件可以直接获得！
'''

'''
如果你把填充色的(0, 0, 0)改为(0, 255, 0)
效果会想黑客帝国的字幕雨一样
我得说,实际试一下并不太像……不过以后你完全可以写一个以假乱真甚至更酷的！
'''