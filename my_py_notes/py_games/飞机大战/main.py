# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-28 上午10:57
# @File    : main.py

# from . import Enemy, HeroPlane, Control
# from . import settings
import pygame
import Enemy, HeroPlane, Control
import settings

def main():
    pygame.init()
    pygame.display.set_caption(settings.GAME_NAME)

    hero = HeroPlane.HeroPlane(240, 550, settings.screen)   # import module 与 from module import 的区别, 前者调用要先加模块名
    enemy = Enemy.Enemy(settings.screen)

    while True:
        settings.screen.blit(settings.bg, (0., 0.))
        hero.display()
        enemy.display()
        pygame.display.update()
        Control.key_control(hero)

if __name__ == '__main__':
    main()
