# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-27 下午6:01
# @File    : 创建surface对象.py

import pygame

'''
一种方法就是刚刚说的pygame.image.load,这个surface有着和图像相同的尺寸和颜色
另外一种方法是指定尺寸创建一个空的surface,下面的语句创建一个256×256像素的surface
'''
# 如果不指定尺寸,那么就创建一个和屏幕大小一样的
bland_surface = pygame.Surface((256, 256))
'''
你还有两个参数可选，第一个是flags：
    HWSURFACE – 类似于前面讲的,更快！不过最好不设定,Pygmae可以自己优化。
    SRCALPHA – 有Alpha通道的surface,如果你需要透明,就要这个选项,这个选项的使用需要第二个参数为32~
    第二个参数是depth, 和pygame.display.set_mode中的一样, 你可以不设定, Pygame会自动设的和display一致。
    不过如果你使用了SRCALPHA，还是设为32吧：
'''
bland_alpha_surface = pygame.Surface((256, 256), flags=pygame.SRCALPHA, depth=32)