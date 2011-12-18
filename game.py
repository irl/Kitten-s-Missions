#!/usr/bin/env python

import pygame

from kmmedia import get_image, get_sound
from kmlevel import Level


if __name__ == "__main__":
	pygame.init()
	pygame.font.init()

	screen = pygame.display.set_mode((640, 400))

	start = get_image('start.png')

	screen.blit(start,(0,0))
	pygame.display.flip()

	running = 1

	while running:
		event = pygame.event.poll()
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE:
				running = 0


	levels = [Level("Beer Run", get_image('bg.png'), get_image('images.png'), 1800, 3150, 3410, get_image('beer.png'), "Beers", 8, get_sound('music.ogg'), get_sound('meow.ogg'), get_image('explode.png'), get_image('loss.png'), get_image('win.png')), Level("Drunken Munch", get_image('bg2.png'), get_image('images.png'), 1000, 3150, 3390, get_image('kebab.png'), "Kebabs", 8, get_sound('music.ogg'), get_sound('meow.ogg'), get_image('explode.png'), get_image('loss.png'), get_image('win.png'), [(1470, 144, 1580, 400), (2087, 144, 2200, 400), (2689, 0, 2796, 202)])]


	for level in levels:
		level.doIntro(screen)
		level.doPlay(screen)
