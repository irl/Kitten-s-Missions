#!/usr/bin/env python

import pygame, sys

from kmmedia import get_image, get_sound
from kmlevel import Level


if __name__ == "__main__":
	try:
		pygame.init()
		pygame.font.init()

		screen = pygame.display.set_mode((640, 400))
		pygame.display.set_caption('Kitten\'s Missions')
		start = get_image('start.png')

		screen.blit(start,(0,0))
		pygame.display.flip()

		running = 1

		while running:
			event = pygame.event.poll()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					running = 0
			elif event.type == pygame.QUIT:
				sys.exit(0)

		screen.blit(get_image('howto.png'),(0,0))
		pygame.display.flip()

		pygame.time.wait(10000)
		

		levels = [Level("Beer Run", get_image('bg.png'), get_image('images.png'), 1800, 3150, 3410, get_image('beer.png'), "Beers", 8, get_sound('music.ogg'), get_sound('meow.ogg'), get_image('explode.png'), get_image('loss.png'), get_image('win.png')), Level("Drunken Munch", get_image('bg2.png'), get_image('images.png'), 1000, 3150, 3390, get_image('kebab.png'), "Kebabs", 8, get_sound('music.ogg'), get_sound('meow.ogg'), get_image('explode.png'), get_image('loss.png'), get_image('win.png'), [(1470, 144, 1580, 400), (2087, 144, 2200, 400), (2689, 0, 2796, 202)])]

		for level in levels:
			level.doIntro(screen)
			level.doPlay(screen)

		score = 0

		pos = 100

		font = pygame.font.Font(None, 36)

		screen.blit(get_image('end.png'), (0,0))

		screen.blit(font.render("Score", 1, (255,255,255)), (10,10))

		for level in levels:
			levelScore = level.g - ( len(level.items.list) - level.g ) - ( level.g % 4 )
			score += levelScore
			screen.blit(font.render("Level \"%s\": %d" % (level.name, levelScore), 1, (255,255,255)), (10, pos))
			pos += 50

		pos += 50

		screen.blit(font.render("Total: %d" % score, 1, (255,255,255)), (10, pos))

		pygame.display.set_caption('Final score')

		pygame.display.flip()

		while True:
			event = pygame.event.poll()
			if event.type == pygame.QUIT:
				sys.exit(0)

	except KeyboardInterrupt:
		sys.exit(0)
