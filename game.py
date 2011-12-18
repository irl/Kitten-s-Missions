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
		

		levels = [Level("Beer Run", get_image('bg.png'), get_image('images.png'), 1800, 3150, 3410, get_image('beer.png'), "Beers", 8, get_sound('music.ogg'), get_sound('meow.ogg'), get_image('explode.png'), get_image('loss.png'), get_image('win.png')), Level("Drunken Munch", get_image('bg2.png'), get_image('images.png'), 1000, 3150, 3390, get_image('kebab.png'), "Kebabs", 8, get_sound('music.ogg'), get_sound('meow.ogg'), get_image('explode.png'), get_image('loss.png'), get_image('win.png'), [(1470, 144, 1580, 400), (2087, 144, 2200, 400), (2689, 0, 2796, 202)]), Level("Must Drink Water", get_image('bg3.png'), get_image('images.png'), 2720, 12255, 12428, get_image('water.png'), "Waters", 50, get_sound('music.ogg'), get_sound('meow.ogg'), get_image('explode.png'), get_image('loss.png'), get_image('win.png'), [(3334,130,3511,197),(3950,257,4132,305),(4390,104,4570,153),(4887,100,5068,150),(4985,294,5169,345),(5548,96,5734,145),(5967,202,6147,255),(7091,101,7269,152),(8169,266,8352,134),(9733,97,9914,146),(10554,282,10736,332),(11414,85,11600,134),(11960,273,12145,327)])]

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
