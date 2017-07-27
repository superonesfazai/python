# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-27 下午6:29
# @File    : 剪裁_clipping_test.py

'''
通常游戏的时候你只需要绘制屏幕的一部分
比如魔兽上面是菜单,下面是操作面板,中间的小兵和英雄打的不可开交时候
上下的部分也是保持相对不动的.
为了实现这一点, surface就有了一种叫裁剪区域(clipping area)的东西
也是一个矩形, 定义了哪部分会被绘制,也就是说一旦定义了这个区域
那么只有这个区域内的像素会被修改,其他的位置保持不变
默认情况下,这个区域是所有地方.
我们可以使用set_clip来设定, 使用get_clip来获得这个区域
'''
# 演示了如何使用这个技术来绘制不同的区域：
import pygame
from pygame.locals import *

screen = pygame.display.set_mode((640, 480), 0, 32)
screen.set_clip(0, 400, 200, 600)
# 在左下角画地图
draw_map()
screen.set_clip(0, 0, 800, 60)
# 在上方画菜单面板
draw_panel()


