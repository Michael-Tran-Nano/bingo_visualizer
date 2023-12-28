import os
import pygame

def load_image(path, alpha=False):
    if alpha:
        img = pygame.image.load(path).convert_alpha()
    else:
        img = pygame.image.load(path).convert()
    return img