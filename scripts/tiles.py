import pygame

class Tiles(pygame.sprite.Sprite):

    def __init__(self, game, no, coordinates):

        super().__init__()
        self.game = game

        self.no = no
        self.image = pygame.image.load(f'tiles/{no}.png').convert()
        self.rect = self.image.get_rect(topleft=coordinates)

        self.drawn = False

        self.coordinates = coordinates
    
    def update(self):
        if self.drawn != self.game.drawn_tiles[self.no-1]:
            self.drawn = not self.drawn

            alpha_value = 50 if self.drawn else 255
            self.image.set_alpha(alpha_value)

    # def render(self, surf):
    #     surf.blit(source=self.image, dest=self.coordinates)

class Plate_tiles(Tiles):
    def __init__(self, game, no, coordinates):
        super().__init__(game, no, coordinates)

        self.rect = self.image.get_rect(center=coordinates)

def tile_collision_checker(tile_group, mouse_pos):
    for tile in tile_group:
        if tile.rect.collidepoint(mouse_pos):
            return tile.no
        
