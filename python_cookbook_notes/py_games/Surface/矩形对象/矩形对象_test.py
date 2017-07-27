# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-27 下午6:22
# @File    : 矩形对象_test.py

from pygame.locals import *
'''
一般来说在制定一个区域的时候,矩形是必须的
比如在屏幕的一部分画东西,在pygame中矩形对象极为常用
它的指定方法可以用一个四元素的元组,或者两个二元素的元组
前两个数为左上坐标, 后两位为右下坐标
'''

'''
Pygame中有一个Rect类,用来存储和处理矩形对象
(包含在pygame.locals中,所以如果你写了from pygame.locals import *就可以直接用这个对象了)
'''
# eg:
my_rect1 = (100, 100, 200, 150)
my_rect2 = ((100, 100), (200, 150))
#上两种为基础方法，表示的矩形也是一样的
my_rect3 = Rect(100, 100, 200, 150)
my_rect4 = Rect((100, 100), (200, 150))

'''
一旦有了Rect对象,我们就可以对其做很多操作
比如调整位置和大小,判断一个点是否在其中等等
以后会慢慢接触到,求知欲旺盛的可以在http://www.pygame.org/docs/ref/rect.html中找到Rect的详细信息
'''