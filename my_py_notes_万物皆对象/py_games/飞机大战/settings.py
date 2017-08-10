# coding = utf-8
__author__ = 'super_fazai'
# @Time    : 17-7-28 下午4:42
# @File    : settings.py
import pygame

SCREEN_SIZE = (480, 853)
GAME_NAME = '飞机大战'
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
bg = pygame.image.load('plane_images/background.png')