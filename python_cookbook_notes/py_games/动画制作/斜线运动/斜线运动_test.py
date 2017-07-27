# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-27 下午10:06
# @File    : 斜线运动_test.py

'''
不再是单纯的直线运动,而是有点像屏保一样,碰到了壁会反弹
不过也并没有新的东西在里面,原理上来说,反弹只不过是把速度取反了而已~
'''

'''
仔细一看的话, 就会明白游戏中的所谓运动(尤其是2D游戏)
不过是把一个物体的坐标改一下而已,不过总是不停的计算和修改x和y
有些麻烦不是么, 下次我们引入向量, 看看使用数学怎样可以帮我们减轻负担
'''

import pygame
from pygame.locals import *
from sys import exit

pygame.init()

screen = pygame.display.set_mode((640, 480), 0, 32)

background = pygame.image.load('../../images/sushiplate.jpg')
sprite = pygame.image.load('../../images/fugu.png')

clock = pygame.time.Clock()

x, y = 100., 100.
speed_x, speed_y = 133., 170.

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    screen.blit(background, (0, 0))
    screen.blit(sprite, (x, y))

    time_passed = clock.tick(30)
    time_passed_seconds = time_passed / 1000.0

    x += speed_x * time_passed_seconds
    y += speed_y * time_passed_seconds

    # 到达边界则把速度反向
    if x > 640 - sprite.get_width():
        speed_x = -speed_x
        x = 640 - sprite.get_width()
    elif x < 0:
        speed_x = -speed_x
        x = 0.

    if y > 480 - sprite.get_height():
        speed_y = -speed_y
        y = 480 - sprite.get_height()
    elif y < 0:
        speed_y = -speed_y
        y = 0

    pygame.display.update()