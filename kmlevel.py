
import pygame
import random
import sys
import openni

class Item:
	def __init__(self, minx, maxx):
		self.x = random.randrange(minx, maxx)
		self.y = random.randrange(0, 349)
		self.g = 0 #has the item been collected?
	def update(self, level):
		if level.x >= (self.x - 345) and level.x <= (self.x - 295) and level.y >= (self.y - 50) and level.y <= (self.y + 100):
			self.g = 1
			level.g += 1

class Items:
	def __init__(self, minx, maxx, num):
		self.list = []
		for c in range(0, num):
			self.list += [Item(minx, maxx)]
	def update(self, level):
		for i in self.list:
			if i.g == 0:
				i.update(level)
	def reset(self):
		for i in self.list:
			i.g = 0


def getClosestPoint(depthMap):

	width = depthMap.width
	height = depthMap.height

	closest = (-1, -1, -1)

	closestDepth = 999999

	for x in range(1, width, 4):
		for y in range(1, height, 3):
			if depthMap[x, y] < closestDepth and depthMap[x,y] is not 0:
				closestDepth = depthMap[x, y]
				closest = (x, y, depthMap[x, y])

	return closest

class Level:
	def __init__(self, name, background, player, start, end, rest, itemImage, itemName, itemCount, music, noise, explode, loss, win, obstacles = []):
		self.name = name
		self.background = background
		self.player = player
		self.start = start
		self.end = end
		self.rest = rest
		self.itemImage = itemImage
		self.itemName = itemName
		self.items = Items(start + 400, end, itemCount)
		self.music = music
		self.noise = noise
		self.explode = explode
		self.loss = loss
		self.win = win
		self.obstacles = obstacles
		self.x = 0
		self.y = 175
		self.xv = 0
		self.yv = 0
		self.g = 0 #items collected in this level
		self.ctx = openni.Context()
		self.ctx.init()
		self.depth = openni.DepthGenerator()
		self.depth.create(self.ctx)
		self.depth.set_resolution_preset(openni.RES_QVGA)
		self.depth.fps = 30
		self.ctx.start_generating_all()

	def render(self, screen, showText = 1, showPlayer = 1):
		global pygame

		screen.blit(self.background, (0 - self.x, 0))

		if showText:
			font = pygame.font.Font(None, 36)
			text = font.render("%s Collected: %d" % (self.itemName, self.g), 1, (0, 0, 0))
			screen.blit(text, (350,0))

		if showPlayer:
			screen.blit(self.player, (295, self.y))

		for i in self.items.list:
			if i.g == 0:
				screen.blit(self.itemImage, (i.x - self.x, i.y))

	def amIDead(self):
		for o in self.obstacles:
			x1, y1, x2, y2 = o
			if self.x >= (x1 - 320) and self.x <= (x2 - 320):
				if self.y >= y1 and self.y <= y2:
					return 1
		return 0

	def doIntro(self, screen):
		pygame.display.set_caption(self.name)
		running = 1
		self.render(screen, 0, 0)
		pygame.display.flip()
		pygame.time.wait(500)
		while self.x < self.start:
			event = pygame.event.poll()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					self.x = self.start
			elif event.type == pygame.QUIT:
				sys.exit(0)
			self.render(screen, 0, 0)
			pygame.display.flip()	
			self.x += 2
			pygame.time.wait(1)

	def doPlay(self, screen):
		notwon = 1

		while notwon:
			running = 1
			death = 0
			self.x = self.start
			self.y = 175
			self.xv = 0
			self.yv = 0

			self.g = 0
			self.items.reset()
	
			pygame.event.clear()

			self.music.play(-1)

			while running:
				event = pygame.event.poll()
		
				if event.type == pygame.QUIT:
					running = 0
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_DOWN:
						self.yv += 5
					elif event.key == pygame.K_UP:
						self.yv -= 5
					elif event.key == pygame.K_RIGHT:
						self.xv += 5
				elif event.type == pygame.KEYUP:
					if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
						self.yv = 0
					elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
						self.xv = 5
		
				self.x += self.xv
				self.y += self.yv

				tmpx, self.y, tmpz = getClosestPoint(self.depth.map)

				if self.y > 330:
					self.y = 330
				if self.y < 0:
					self.y = 0
	
				if self.x >= self.end:
					self.music.stop()
					self.noise.play()
					while self.x < self.rest:
						self.x += 5
						self.y = ( self.y + self.y + 330 ) / 3
						self.render(screen)
						pygame.display.flip()
					running = 0

				if self.amIDead():
					death = 1
					self.music.stop()
					self.noise.play()
					sub = screen.subsurface((295, self.y), (50, 50))
					for c in range(0, 5):
						sub.blit(self.explode, (0 - (c * 50),0))
						pygame.display.flip()
						pygame.time.wait(200)
					while 1:
						for c in range(0, 5):
							sub.blit(self.explode, (0 - (c * 50),0))
							pygame.time.wait(200)
							screen.blit(self.loss, (0,0))
							pygame.display.flip()
							event = pygame.event.poll()
							if event.type == pygame.KEYUP:
								if event.key == pygame.K_SPACE:
									running = 0
									break
							elif event.type == pygame.QUIT:
								sys.exit(0)
						if running == 0:
							break

				if death:
					break

				self.items.update(self)
	
				self.render(screen)
				pygame.display.flip()

			if death:
				continue			

			self.render(screen, 0)
			screen.blit(self.win, (0,0))

			font = pygame.font.Font(None, 36)
	
			if self.g < 4:
				text = font.render("You did not collect enough %s for everyone" % self.itemName, 1, (0, 0, 0))
				screen.blit(text, (30,170))
			else:
				text = font.render("You collected %d %s. That's %d each with %d leftover!" % (self.g, self.itemName, self.g / 4, self.g % 4), 1, (0, 0, 0))
				screen.blit(text, (5,170))

				notwon = 0
	
			pygame.display.flip()
	
			pygame.time.wait(5000)
