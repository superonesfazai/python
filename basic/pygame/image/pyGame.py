# -*- coding:utf-8 -*-
# file: pyGame.py
#
import sys 
import pygame
import threading
import random
class Game:
	def __init__(self):
		pygame.init()
		self.total = 0
		self.you = 0
		self.python = 0
		self.screen = pygame.display.set_mode((800,600))
		self.image = []
		self.imagerect = []
		self.bimage = pygame.image.load('image/2.gif')
		self.vs = pygame.image.load('image/vs.gif')
		self.o = pygame.image.load('image/o.gif')
		self.p = pygame.image.load('image/p.gif')
		self.u = pygame.image.load('image/u.gif')
		for i in range(3):
			gif = pygame.image.load('image/' + str(i) + '.gif')
			self.image.append(gif)
		for i in range(3):
			image = self.image[i]
			rect = image.get_rect()
			rect.left = 200 * (i+1) + rect.left
			rect.top = 400
			self.imagerect.append(rect)
	def run(self):
		for i in range(3):
			self.screen.blit(self.image[i], self.imagerect[i])
		pygame.display.flip()
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					self.OnMouseButDown()
					self.result = pygame.image.fromstring(str(self.you),(1,1), 'RGB')
					self.screen.blit(self.result, (10,10, 100, 100))
				else:
					pass
	def OnMouseButDown(self):
		self.total = self.total + 1
		self.screen.blit(self.vs, (300, 150, 140, 140))
		pos = pygame.mouse.get_pos()
		if pos[1] > 400 and pos[1] < 540:
			if pos[0] > 200 and pos[0] < 340:
				self.screen.blit(self.image[0], (150 ,150, 140,140))
				value = 0
				self.isWin(0)
			elif pos[0] > 400 and pos[0] < 540:
				self.screen.blit(self.image[1], (150 ,150, 140,140))
				value = 1
				self.isWin(1)
			elif pos[0] > 600 and pos[0] < 740:
				self.screen.blit(self.image[2], (150 ,150, 140,140))
				value = 2
				self.isWin(2)
			else:
				pass
	def isWin(self, value):
		num = random.randint(0, 2)
		self.screen.blit(self.image[num], (450 ,150, 590,240))
		pygame.display.flip()
		if num == value:
			self.screen.blit(self.o, (220, 10, 140, 70))
			pygame.display.flip()
		elif num < value:
			if num == 0:
				self.screen.blit(self.p, (220, 10, 140, 70))
				pygame.display.flip()
				self.python = self.python + 1
			else:
				self.screen.blit(self.u, (220, 10, 140, 70))
				pygame.display.flip()
				self.you = self.you + 1
		else:
			if num == 2:
				self.screen.blit(self.p, (220, 10, 140, 70))
				pygame.display.flip()
				self.python = self.python + 1
			else:
				self.screen.blit(self.u, (220, 10, 140, 70))
				pygame.display.flip()
				self.you = self.you + 1

game = Game()
game.run()
