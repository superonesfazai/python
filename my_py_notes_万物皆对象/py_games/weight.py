import sys
import pygame
from pygame.locals import *
import random
import time
import math

"""
    x = a*(2*cos(t)-cos(2*t))
    y = a*(2*sin(t)-sin(2*t))
    x = r*(t-sin(t))
    y = r*(1-cos(t))
"""


class Weight(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # 在画sprite时使用的图像和矩形
        self.image = weight_image
        self.rect = self.image.get_rect()
        # self.reset()
        # self.forward = random.randint(1, 8)
        self.x = 700
        self.y = 350
        self.a = 20
        self.big = False
        self.t = 0

    def reset(self):
        """
        将图移动到屏幕顶端的随机位置
        :return: 
        """
        # self.rect.top = -self.rect.height
        # self.rect.top = random.randrange(screen_size[1] - 100)
        # self.rect.centerx = random.randrange(screen_size[0] - 100)
        # self.rect.top = 350
        # self.rect.centerx = 0
        # while self.rect.centerx % 100 != 0:
        #     self.rect.centerx += 1

    def update(self):
        self.t += random.random()
        self.rect.top = self.a * (2 * math.cos(self.t) - math.cos(2 * self.t)) + 450
        self.rect.top = screen_size[1] - self.rect.top
        self.rect.centerx = self.a * (2 * math.sin(self.t) - math.sin(2 * self.t)) + 700
        self.rect.centerx = screen_size[0] - self.rect.centerx
        self.t += 0.5
        if self.big:
            self.a -= 1
        else:
            self.a += 1
        if self.a > 100:
            self.big = True
        if self.a < 20:
            self.big = False
        time.sleep(0.0001)

    def update3(self):
        self.rect.centerx += 50
        # print(math.sin(self.x) * 10)
        self.rect.top = 350 + math.sin(self.x) * 150
        self.x += 0.5
        self.check()

    def check3(self):
        # if self.rect.top > screen_size[1]:
        # self.reset()
        # math.
        if self.rect.centerx > screen_size[0]:
            self.rect.centerx = self.rect.centerx - screen_size[0]
            # if self.rect.top < 0:
            #     self.reset()
            # if self.rect.centerx < 0:
            #     self.reset()

    def update2(self):
        if self.forward == 1:
            self.rect.top -= 1
            self.rect.centerx -= 1
            self.check()
        if self.forward == 2:
            self.rect.top -= 1
            self.check()
        if self.forward == 3:
            self.rect.top -= 1
            self.rect.centerx += 1
            self.check()
        if self.forward == 4:
            # self.rect.top -= 1
            self.rect.centerx -= 1
            self.check()
        if self.forward == 5:
            self.forward = random.randint(1, 8)
            # self.rect.top -= 1
            # self.rect.centerx -= 1
            # self.check()
        if self.forward == 6:
            # self.rect.top =
            self.rect.centerx += 1
            self.check()
        if self.forward == 7:
            self.rect.top += 1
            self.rect.centerx -= 1
            self.check()
        if self.forward == 8:
            self.rect.top += 1
            self.rect.centerx += 1
            self.check()
            # if self.rect.top > screen_size[1] or self.rect.centerx > screen_size[0]:
            #     self.reset()

    def check2(self):
        if self.rect.top > screen_size[1] - 100:
            self.rect.top -= 4
            self.forward = random.randint(1, 8)
        if self.rect.centerx > screen_size[0] - 48:
            self.rect.centerx -= 4
            self.forward = random.randint(1, 8)
        if self.rect.top < 0:
            self.rect.top += 4
            self.forward = random.randint(1, 8)
        if self.rect.centerx < 48:
            self.rect.centerx += 4
            self.forward = random.randint(1, 8)

    def check1(self):
        if self.rect.top > screen_size[1]:
            self.rect.top -= 2
        if self.rect.centerx > screen_size[0]:
            self.rect.centerx -= 2
        if self.rect.top < 0:
            self.rect.top += 2
        if self.rect.centerx < 0:
            self.rect.centerx += 2

    def update1(self):
        change = random.randint(1, 8)
        if change == 1:
            self.rect.top -= 4
            self.rect.centerx -= 4
            self.check()
        if change == 2:
            self.rect.top -= 4
            self.check()
        if change == 3:
            self.rect.top -= 4
            self.rect.centerx += 4
            self.check()
        if change == 4:
            # self.rect.top -= 1
            self.rect.centerx -= 4
            self.check()
        if change == 5:
            pass
            # self.rect.top -= 1
            # self.rect.centerx -= 1
            # self.check()
        if change == 6:
            # self.rect.top =
            self.rect.centerx += 4
            self.check()
        if change == 7:
            self.rect.top += 4
            self.rect.centerx -= 4
            self.check()
        if change == 7:
            self.rect.top += 4
            # self.rect.centerx -= 1
            self.check()
        if change == 7:
            self.rect.top += 4
            self.rect.centerx += 4
            self.check()
            # if self.rect.top > screen_size[1] or self.rect.centerx > screen_size[0]:
            #     self.reset()



# 初始化
pygame.init()
screen_size = (1366, 768)
pygame.display.set_mode(screen_size, FULLSCREEN)
pygame.mouse.set_visible(1)
# 载入图像
weight_image = pygame.image.load('weight.gif')
weight_image = weight_image.convert()
# print(Linus_image)
# 创建一个子图形组
sprites = pygame.sprite.RenderUpdates()
for i in range(200):
    sprites.add(Weight())
# 获取屏幕表面，并且填充
screen = pygame.display.get_surface()
bg = (255, 255, 255)
screen.fill(bg)
pygame.display.flip()


# 用于清除子图形
def clear_callback(surf, rect):
    surf.fill(bg, rect)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()
    sprites.clear(screen, clear_callback)
    sprites.update()
    updates = sprites.draw(screen)
    pygame.display.update(updates)
