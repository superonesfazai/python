# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-28 下午4:35
# @File    : HeroPlane.py

import pygame

class HeroPlane():
    def __init__(self, hero_x, hero_y, screen):
        '''初始化飞机'''
        self.image = pygame.image.load('plane_images/hero.gif')
        self.hero_x = hero_x
        self.hero_y = hero_y
        self.screen = screen

    def display(self):
        '''显示飞机'''
        self.screen.blit(self.image, (self.hero_x, self.hero_y))

    def move_left(self):
        self.hero_x -= 5
    def move_right(self):
        self.hero_x += 5
    def move_up(self):
        self.hero_y -= 5
    def move_down(self):
        self.hero_y += 5