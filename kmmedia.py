
import pygame, os

_image_library = {}

def get_image(path):
	global pygame
        global _image_library
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path)
                _image_library[path] = image
        return image

def get_sound(path):
	global pygame
	return pygame.mixer.Sound(path)
