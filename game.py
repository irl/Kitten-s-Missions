#!/usr/bin/env python

import pygame
import os
import random

_image_library = {}

def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path)
                _image_library[path] = image
        return image

def get_sound(path):
	return pygame.mixer.Sound(path)

class Bottle:
	def __init__(self):
		self.x = random.randrange(2340, 3150)
		self.y = random.randrange(0, 349)
		self.g = 0

class Kebab:
	def __init__(self):
		self.x = random.randrange(1500, 3150)
		self.y = random.randrange(0, 349)
		self.g = 0

bottles = []

for c in range(0, 8):
	bottles += [Bottle()]

running = 1

pygame.init()
pygame.font.init()

x = 0
y = 175
xv = 0
yv = 1
beer = 0

screen = pygame.display.set_mode((640, 400))
image = get_image('images.png')
background = get_image('bg.png')
start = get_image('start.png')
bottle = get_image('beer.png')
meow = get_sound('meow.ogg')
explode = get_image('explode.png')
loss = get_image('loss.png')
music = get_sound('music.ogg')

screen.blit(start,(0,0))
pygame.display.flip()

while running:
	event = pygame.event.poll()
	if event.type == pygame.KEYUP:
		if event.key == pygame.K_SPACE:
			running = 0

running = 1

screen.blit(background, (0,0))
pygame.display.flip()

pygame.time.wait(500)

while x < 1800:
	screen.blit(background, (0-x,0))
	pygame.display.flip()
	x += 2
	pygame.time.wait(1)
#x = 3251

music.play(-1)

while running:
	event = pygame.event.poll()

	if event.type == pygame.QUIT:
		running = 0
	elif event.type == pygame.KEYDOWN:
		if event.key == pygame.K_DOWN:
			yv += 5
		elif event.key == pygame.K_UP:
			yv -= 5
		elif event.key == pygame.K_RIGHT:
			xv += 5
	elif event.type == pygame.KEYUP:
		if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
			yv = 1
		elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
			xv = 3

	x += xv
	y += yv

	if y > 330:
		y = 330

	if y < 0:
		y = 0
		meow.play()

	if x >= 3250:
		music.stop()
		meow.play()
		while x < 3410:
			x += 1
			y = ( y + y + 330 ) / 3
			screen.blit(background, (0-x,0))
			screen.blit(image, ((640/2)-25, y))
			font = pygame.font.Font(None, 36)
			text = font.render("Beer Collected: %d" % beer, 1, (0, 0, 0))
			screen.blit(text, (410,0))
			pygame.display.flip()
		running = 0

	screen.blit(background, (0-x,0))

	screen.blit(image, ((640/2)-25, y))

	for b in bottles:
		if b.g == 0:
			screen.blit(bottle, (b.x-x,b.y))
			if x >= (b.x - 345) and x <= (b.x - 295) and y >= (b.y - 50) and y <= (b.y + 100):
				b.g = 1
				beer += 1

	font = pygame.font.Font(None, 36)
	text = font.render("Beer Collected: %d" % beer, 1, (0, 0, 0))
	screen.blit(text, (410,0))

	pygame.display.flip()

win = get_image('win.png')

screen.blit(background, (0-x,0))
screen.blit(image, ((640/2)-25, y))
screen.blit(win, (0,0))

if beer < 4:
	text = font.render("You did not collect enough beers for everyone", 1, (0, 0, 0))
	screen.blit(text, (40,170))
else:
	text = font.render("You collected %d beers. That's %d each with %d leftover!" % (beer, beer / 4, beer % 4), 1, (0, 0, 0))
	screen.blit(text, (20,170))

pygame.display.flip()

pygame.time.wait(2000)

"""Level Two"""

x = 0

background = get_image('bg2.png')
kebab = get_image('kebab.png')

screen.blit(background, (0,0))
pygame.display.flip()

pygame.time.wait(500)

while x < 1000:
	screen.blit(background, (0-x,0))
	pygame.display.flip()
	x += 2
	pygame.time.wait(1)

wonthegame = 1

while wonthegame:
	
	kebabs = []
	
	for c in range(0, 8):
		kebabs += [Kebab()]
	
	running = 1
	kebabscollected = 0
	
	x = 1000
	y = 175

	xv = 0
	yv = 1

	music.play(-1)

	while running:
		event = pygame.event.poll()
	
		if event.type == pygame.QUIT:
			running = 0
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				yv += 5
			elif event.key == pygame.K_UP:
				yv -= 5
			elif event.key == pygame.K_RIGHT:
				xv += 5
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
				yv = 1
			elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				xv = 4
	
		x += xv
		y += yv
	
		if y > 330:
			y = 330
	
		if y < 0:
			y = 0
			meow.play()
	
		if x >= 3250:
			music.stop()
			meow.play()
			while x < 3390:
				x += 1
				y = ( y + y + 330 ) / 3
				screen.blit(background, (0-x,0))
				screen.blit(image, ((640/2)-25, y))
				font = pygame.font.Font(None, 36)
				text = font.render("Kebabs Collected: %d" % kebabscollected, 1, (0, 0, 0))
				screen.blit(text, (370,0))
				pygame.display.flip()
			running = 0
			wonthegame = 0
	

		cactusdeath = 0

		if ( x >= (1470 - 320) and x <= (1580 - 320) ) or ( x >= (2087 - 320) and x <= (2200 - 320) ):
			if y > 144:
				cactusdeath = 1

		if ( x >= (2689 - 320) and x <= (2796 - 320) ):
			if y < 202:
				cactusdeath = 1
	
		if cactusdeath:
			music.stop()
			meow.play()
			sub = screen.subsurface((295, y), (50, 50))
			for c in range(0, 5):
				sub.blit(explode, (0 - (c * 50),0))
				pygame.display.flip()
				pygame.time.wait(200)
			screen.blit(loss, (0,0))
			pygame.display.flip()
			while 1:
				sub.blit(explode, (0 - (c * 50),0))
				pygame.time.wait(200)
				screen.blit(loss, (0,0))
				pygame.display.flip()
				event = pygame.event.poll()
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_SPACE:
						running = 0
						break
	
		screen.blit(background, (0-x,0))
	
		screen.blit(image, ((640/2)-25, y))
	
		for b in kebabs:
			if b.g == 0:
				screen.blit(kebab, (b.x-x,b.y))
				if x >= (b.x - 345) and x <= (b.x - 220) and y >= (b.y - 50) and y <= (b.y + 100):
					b.g = 1
					kebabscollected += 1
	
		font = pygame.font.Font(None, 36)
		text = font.render("Kebabs Collected: %d" % kebabscollected, 1, (0, 0, 0))
		screen.blit(text, (370,0))
	
		pygame.display.flip()

screen.blit(background, (0-x,0))
screen.blit(image, ((640/2)-25, y))
screen.blit(win, (0,0))

if kebabscollected < 4:
	text = font.render("You did not collect enough kebabs for everyone", 1, (0, 0, 0))
	screen.blit(text, (40,170))
else:
	text = font.render("You collected %d kebabs. That's %d each with %d leftover!" % (kebabscollected, kebabscollected / 4, kebabscollected % 4), 1, (0, 0, 0))
	screen.blit(text, (5,170))

pygame.display.flip()

pygame.time.wait(2000)

end = get_image('end.png')

screen.blit(end, (0,0))

f = pygame.font.Font(None, 36)

youwin = f.render("You Win!", 1, (255,255,255))
totalbeers = f.render("Total Beers: %d" % beer, 1, (255,255,255))
totalkebabs = f.render("Total Kebabs: %d" % kebabscollected, 1, (255,255,255))

screen.blit(youwin, (275,150))
screen.blit(totalbeers, (250,190))
screen.blit(totalkebabs, (240,230))

pygame.display.flip()

while 1:
	pass
