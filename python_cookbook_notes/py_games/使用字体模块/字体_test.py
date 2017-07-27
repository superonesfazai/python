# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-27 上午11:47
# @File    : 字体_test.py

import pygame
# Pygame可以直接调用系统字体,或者也可以使用TTF字体
# eg:
# 为了使用字体,你得先创建一个Font对象
# 第一个参数是字体名,第二个自然就是大小
my_font = pygame.font.SysFont("unbatang", 16)

# 你也可以使用pygame.font.get_fonts()来获得当前系统所有可用字体
# 还有一个更好的方法的, 使用TTF的方法：
# 这个语句使用了一个叫做'my_font.ttf'
# 这个方法之所以好是因为你可以把字体文件随游戏一起分发
# 避免用户机器上没有需要的字体
my_font = pygame.font.Font("my_font.ttf", 16)

# 一旦你创建了一个font对象
# 你就可以使用render方法来写字了
# 然后就能blit到屏幕上
# 第一个参数是写的文字
# 第二个参数是个布尔值,以为这是否开启抗锯齿,就是说True的话字体会比较平滑,不过相应的速度有一点点影响
# 第三个参数是字体的颜色
# 第四个是背景色,如果你想没有背景色(也就是透明),那么可以不加这第四个参数。
text_surface = my_font.render("Pygame is cool!", True, (0, 0, 0), (255, 255, 255))

# 下面是一个小例子演示下文字的使用,不过并不是显示在屏幕上,而是存成一个图片文件
import pygame

my_name = 'super_fazai'
pygame.init()

my_font = pygame.font.SysFont('arial', 64)
name_surface = my_font.render(my_name, True, (0, 0, 0), (255, 255, 255))
pygame.image.save(name_surface, 'name.png')