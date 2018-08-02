# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-28 下午4:36
# @File    : Enemy.py
# import sys
# sys.path.append('.')

import pygame
from random import randint
from settings import bg

class Enemy():
    def __init__(self, screen):
        self.enemy_x = randint(0, 400)
        self.enemy_y = 0
        self.image = pygame.image.load('plane_images/enemy0.png')
        self.screen = screen
        self.speed = 250.

    def display(self):
        click = pygame.time.Clock()
        while True:
            self.screen.blit(bg, (0, 0))
            self.screen.blit(self.image, (self.enemy_x, self.enemy_y))

            time_passed = click.tick()
            time_passed_seconds = time_passed / 2000.
            distance_moved = time_passed_seconds * self.speed

            if self.enemy_x < 480:
                self.enemy_x += distance_moved

            elif self.enemy_x > 480:
                self.enemy_x = 0
            # pygame.display.update()