
# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-28 下午4:36
# @File    : Laser.py

import pygame

class Laser():
    def __init__(self, laser_x, laser_y, screen):
        self.laser_x = laser_x
        self.laser_y = laser_y
        self.screen = screen
        self.image = pygame.image.load('plane_images/bullet.png')
        self.speed = 250.

    def display(self):
        '''显示子弹'''
        # click = pygame.time.Clock()
        height, width = self.image.get_size()
        print(height, ' ', width)
        while True:
            self.screen.blit(self.image, (self.laser_x + int(width * 1.8), self.laser_y - int(height)))

            # time_passed = click.tick()
            # time_passed_seconds = time_passed / 1000.
            # distance = time_passed_seconds * self.speed
            self.laser_y -= 50

            if not (self.laser_y):
                break
            pygame.display.update()