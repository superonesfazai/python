# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-27 上午10:30
# @File    : 产生事件_test.py

'''
通常玩家做什么,Pygame就产生对应的事件就可以了
不过有的时候我们需要模拟出一些事件来
比如录像回放的时候, 我们就要把用户的操作再现一遍。
'''

# 为了产生事件,必须先造一个出来,然后再传递它
import pygame
from pygame.locals import *

pygame.init()
my_event = pygame.event.Event(KEYDOWN, key=K_SPACE, mod=0, unicode=u' ')
# 你也可以像下面这样写,看起来比较清晰
my_event = pygame.event.Event(KEYDOWN, {"key":K_SPACE, "mod":0, "unicode":u' '})
pygame.event.post(my_event)

# 你甚至可以产生一个完全自定义的全新事件
import pygame
from pygame.locals import *

pygame.init()
CATONKEYBOARD = USEREVENT + 1
my_event = pygame.event.Event(CATONKEYBOARD, message='Bad cat!')
pygame.event.post(my_event)

# 然后获得它
for event in pygame.event.get():
    if event.type == CATONKEYBOARD:
        print(event.message)