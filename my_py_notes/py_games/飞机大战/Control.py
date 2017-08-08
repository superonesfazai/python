# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-28 下午4:38
# @File    : Control.py
# import sys
# sys.path.append('.')

import pygame
from pygame.locals import *
# from . import Laser
# from . import settings
import Laser
import settings

class Control():
    def key_control(hero):
        for event in pygame.event.get():
            if event.type == QUIT:
                print('exit')
                exit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT or event.key == K_d:
                    hero.move_right()
                    hero.display()
                    print('right')
                elif event.key == K_LEFT or event.key == K_a:
                    hero.move_left()
                    hero.display()
                    print('left')
                elif event.key == K_UP or event.key == K_w:
                    hero.move_up()
                    hero.display()
                    print('up')
                elif event.key == K_DOWN or event.key == K_s:
                    hero.move_down()
                    hero.move_down()
                    print('down')
                elif event.key == K_SPACE:
                    print('发射')
                    tmp_x = hero.hero_x
                    tmp_y = hero.hero_y
                    tmp_laser = Laser(tmp_x, tmp_y, screen)
                    tmp_laser.display()
                    del tmp_laser
                    pass
            elif event.type == KEYUP:
                move_x, move_y = 0, 0

            # screen.fill((0, 0, 0))
            settings.screen.blit(bg, (0, 0))
            hero.display()
            # print(hero.hero_x, ' ', hero.hero_y)
            pygame.display.update()