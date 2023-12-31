import pygame

def img_obj(path, pos, alpha=False):
    if alpha:
        img = pygame.image.load(path).convert_alpha()
    else:
        img = pygame.image.load(path).convert()

    rect = img.get_rect(**pos)

    return [img, rect]