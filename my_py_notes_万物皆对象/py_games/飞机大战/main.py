# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-28 上午10:57
# @File    : main.py

import pygame
from Enemy import Enemy
from HeroPlane import HeroPlane
from Control import Control
from settings import (
    GAME_NAME,
    screen,
    bg,
)
# import Enemy, HeroPlane, Control
# import settings

def main():
    pygame.init()
    pygame.display.set_caption(GAME_NAME)

    hero = HeroPlane(240, 550, screen)   # import module 与 from module import 的区别, 前者调用要先加模块名
    enemy = Enemy(screen)

    while True:
        screen.blit(bg, (0., 0.))
        hero.display()
        enemy.display()
        pygame.display.update()
        Control.key_control(hero)

if __name__ == '__main__':
    main()
