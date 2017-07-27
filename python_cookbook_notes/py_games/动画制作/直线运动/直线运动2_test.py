# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-27 下午9:56
# @File    : 直线运动2_test.py

'''
我们把上面的结论实际试用一下,假设让我们的小鱼儿每秒游动250像素,
这样游动一个屏幕差不多需要2.56秒.我们就需要知道,
从上一帧开始到现在,小鱼应该游动了多少像素,这个算法很简单,速度*时间就行了,
也就是250 * time_passed_second.不过我们刚刚得到的time_passed是毫秒
不要忘了除以1000.0, 当然我们也能假设小鱼每毫秒游动0.25像素,这样就可以直接乘了
不过这样的速度单位有些怪怪的……
'''
# 不同屏幕上的鱼的速度都是一致的了.请牢牢记住这个方法
# 在很多情况下,通过时间控制要比直接调节帧率好用的多
import pygame
from pygame.locals import *
from sys import exit

pygame.init()

screen = pygame.display.set_mode((640, 480), 0, 32)

bg = pygame.image.load('../../images/sushiplate.jpg')
sprite = pygame.image.load('../../images/fugu.png')

# Clock对象
clock = pygame.time.Clock()

x = 0.
# 速度(像素/秒)
speed = 250.

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    screen.blit(bg, (0, 0))
    screen.blit(sprite, (x, 100))

    time_passed = clock.tick()
    time_passed_seconds = time_passed / 1000.0

    distance_moved = time_passed_seconds * speed
    x += distance_moved

    # 想一下，这里减去640和直接归零有何不同？
    if x > 640.:
        x -= 640.

    pygame.display.update()