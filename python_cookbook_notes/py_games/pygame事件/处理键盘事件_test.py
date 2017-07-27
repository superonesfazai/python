# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-27 上午10:02
# @File    : 处理键盘事件_test.py

import pygame
from pygame.locals import *
from sys import exit


pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
bg = pygame.image.load('../images/sushiplate.jpg')

x, y = 0, 0
move_x, move_y = 0, 0

while True:
    for event in pygame.event.get():
        if event.type is QUIT:
            exit()
        if event.type == KEYDOWN:       # 判断键盘是否按下
            if event.key == K_LEFT:     # 按下的是左方向键, 坐标减1
                move_x = -1
            elif event.key == K_RIGHT:  # 右方向键则加1
                move_x = 1
            elif event.key == K_UP:
                move_y = -1
            elif event.key == K_DOWN:
                move_y = 1
        elif event.type == KEYUP:       # 如果用户放开了键盘,图就不要动了
            move_x = 0
            move_y = 0

        # 计算出新的坐标
        x += move_x
        y += move_y

        screen.fill((0, 0, 0))
        screen.blit(bg, (x, y))

        # 在新的位置上画图
        pygame.display.update()

'''
当我们运行这个程序的时候,按下方向键就可以把背景图移动,但是等等！
为什么我只能按一下动一下啊……太不好试了吧？！
用脚掌考虑下就应该按着就一直动下去才是啊！？Pygame这么垃圾么……
哈哈哈哈哈哈
'''

'''
KEYDOWN和KEYUP的参数描述如下：
    key – 按下或者放开的键值,是一个数字,估计地球上很少有人可以记住,所以Pygame中你可以使用K_xxx来表示,比如字母a就是K_a,还有K_SPACE和K_RETURN等。
    mod – 包含了组合键信息,如果mod & KMOD_CTRL是真的话,表示用户同时按下了Ctrl键,类似的还有KMOD_SHIFT,KMOD_ALT。
    unicode – 代表了按下键的Unicode值,这个有点不好理解,真正说清楚又太麻烦,游戏中也不太常用,说明暂时省略，什么时候需要再讲吧。
'''
