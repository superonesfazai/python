# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-28 下午5:32
# @File    : plane.py

import pygame
from pygame.locals import *
from random import randint
import time

SCREEN_SIZE = (480, 853)
GAME_NAME = '飞机大战'
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
bg = pygame.image.load('plane_images/background.png')

class BaseLaser():
    '''子弹基类'''
    def __init__(self, x, y, screen, img_str):
        self.x = x
        self.y = y
        self.screen = screen
        # 图片
        self.image = pygame.image.load(img_str)

    def display(self):
        '''显示子弹'''
        self.screen.blit(self.image, (self.x, self.y))

class BasePlane():
    def __init__(self, x, y, screen, img_str):
        self.x = x
        self.y = y
        self.screen = screen
        self.image = pygame.image.load(img_str)
        self.lasers = []        # # 定义一个子弹列表, 用于记录发出的所有列表

class HeroPlaneLaser(BaseLaser):      # 子弹类
    def __init__(self, x, y, screen):
        super().__init__(x, y, screen, './plane_images/bullet.png')

    def move(self):
        self.y -= 10

    def get_image_size(self):       # 返回子弹图片的高,和宽
        height, width = self.image.get_size()
        return height, width

class EnemyPlaneLaser(BaseLaser):
    def __init__(self, x, y, screen):
        laser_type = randint(1, 2)
        image_path = './plane_images/bullet%d.png' % laser_type
        super().__init__(x, y, screen, image_path)

    def move(self):
        self.y += 5

    def get_image_size(self):       # 返回子弹图片的高,和宽
        height, width = self.image.get_size()
        return height, width

class HeroPlane(BasePlane):
    def __init__(self, x, y, screen):
        '''初始化飞机'''
        super().__init__(x, y, screen, './plane_images/hero.gif')

    def display(self):
        '''显示飞机'''
        self.screen.blit(self.image, (self.x, self.y))

        # 创建临时的列表,用于记录需要被删除的子弹
        out_screen_lasers = []

        # 先判断哪个子弹是否超出边界, 如超出则将子弹删除
        # 切记不要边遍历, 边增删, 否则会遗漏
        for laser in self.lasers:
            if laser.y < 0:
                out_screen_lasers.append(laser)

        # 遍历临时列表,逐个删除越界的子弹
        for laser in out_screen_lasers:
            self.lasers.remove(laser)
        # 子弹不仅要在发射是显示, 在整个飞行过程中始终都要显示,可以将子弹的显示封装到飞机的显示中去
        for laser in self.lasers:
            laser.display()
            laser.move()

    def move_left(self):
        self.x -= 5
    def move_right(self):
        self.x += 5
    def move_up(self):
        self.y -= 5
    def move_down(self):
        self.y += 5

    def fire(self):     # 开火
        # 子弹的位置: x:飞机的起始绘图位置x+飞机图片x的1/2-子弹图片x
        height, width = self.image.get_size()     # 获取飞机图片的位置
        tmp_laser = HeroPlaneLaser(1, 2, screen)     # 用于临时取照片的大小
        new_laser = HeroPlaneLaser(self.x + width / 2 - tmp_laser.get_image_size()[1], self.y - tmp_laser.get_image_size()[0], self.screen)
        self.lasers.append(new_laser)
        new_laser.display()

class EnemyPlane(BasePlane):
    def __init__(self, x, y, screen):
        enemy_number = randint(0, 2)
        image_path = 'plane_images/enemy%d.png' % enemy_number
        super().__init__(x, y, screen, image_path)

        # 记录飞机的方向
        self.is_direction_right = True

    def display(self):
        # # click = pygame.time.Clock()     # 自己原先写的方法
        # while True:
        #     # self.screen.blit(bg, (0, 0))
        #     self.screen.blit(self.image, (self.enemy_x, self.enemy_y))
        #
        #     # time_passed = click.tick()
        #     # time_passed_seconds = time_passed / 2000.
        #     # distance_moved = time_passed_seconds * self.speed
        #
        #     # image_pos = self.image.get_rect()
        #     # self.screen.blit(self.image, image_pos)
        #     pygame.time.delay(100)
        #
        #     if self.enemy_x < 480:
        #         self.enemy_x += 10        # distance_moved
        #
        #     elif self.enemy_x > 480:
        #         self.enemy_x = 0
        #     pygame.display.update()
        self.screen.blit(self.image, (self.x, self.y))

        out_screen_lasers =   []
        for laser in self.lasers:
            if laser.y > 853:
                out_screen_lasers.append(laser)
        for laser in out_screen_lasers:
            self.lasers.remove(laser)

        for laser in self.lasers:
            laser.display()
            laser.move()

    def move(self):     # 敌机移动
        # 根据飞机的方向移动
        if self.is_direction_right:     # 如果飞机往右飞
            self.x += 5
        else:                           # 往左飞
            self.x -= 5
        if self.x > (480-self.get_image_size()[1]):
            self.is_direction_right = False
        elif self.x < 0:
            self.is_direction_right = True

    def fire(self):     # 敌机开火
        # 通过生成一个随机数, 来随机生成一个子弹
        num = randint(1, 50)
        if num == 25:
            height, width = self.image.get_size()  # 获取飞机图片的位置
            tmp_laser = EnemyPlaneLaser(1, 2, screen)  # 用于临时取照片的大小
            new_laser = EnemyPlaneLaser(self.x + width / 2 - tmp_laser.get_image_size()[1],
                                   self.y + height + tmp_laser.get_image_size()[0], self.screen)
            self.lasers.append(new_laser)
            new_laser.display()

    def get_image_size(self):
        height, width = self.image.get_size()
        return height, width

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
                    # tmp_x = hero.hero_x
                    # tmp_y = hero.hero_y
                    # tmp_laser = Laser(tmp_x, tmp_y, screen)
                    # tmp_laser.display()
                    # del tmp_laser
                    hero.fire()
                    pass
            elif event.type == KEYUP:
                move_x, move_y = 0, 0

            # screen.fill((0, 0, 0))
            screen.blit(bg, (0, 0))
            hero.display()
            # print(hero.hero_x, ' ', hero.hero_y)
            pygame.display.update()

def main():
    pygame.init()
    pygame.display.set_caption(GAME_NAME)

    hero = HeroPlane(240, 550, screen)   # import module 与 from module import 的区别, 前者调用要先加模块名
    enemy = EnemyPlane(200, 50, screen)
    enemy1 = EnemyPlane(150, 100, screen)
    enemy2 = EnemyPlane(300, 200, screen)

    while True:
        screen.blit(bg, (0., 0.))
        hero.display()
        enemy.display()
        enemy.move()
        # 敌机开火
        enemy.fire()

        enemy1.display()
        enemy1.move()
        enemy1.fire()

        enemy2.display()
        enemy2.move()
        enemy2.fire()
        pygame.display.update()
        Control.key_control(hero)
        # 为了不让程序刷新过快, 以及占用cpu太多, 可以让程序进行一定的延迟
        time.sleep(0.02)

if __name__ == '__main__':
    main()
