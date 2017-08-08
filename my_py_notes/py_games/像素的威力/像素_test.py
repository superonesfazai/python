# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-27 下午12:30
# @File    : 像素_test.py

import pygame

pygame.init()

screen = pygame.display.set_mode((640, 480))

all_colors = pygame.Surface((4096, 4096), depth=24)

for r in range(256):
    print(r + 1, 'out of 256')
    x = (r & 15) * 256
    y = (r >> 4) * 256
    for g in range(256):
        for b in range(256):
            all_colors.set_at((x + g, y + b), (r, g, b))

pygame.image.save(all_colors, 'allcolors.bmp')

# 能生成一个53MB左右的bmp位图