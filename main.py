import pygame
from sys import exit

# Settings
window_size = (900, 450)

class Bingo_tile(pygame.sprite.Sprite):
    def __init__(self, no, coordinates, plate=False):
        super().__init__()
        self.image = pygame.image.load(f'tiles/{no}.png').convert()
        if plate:
            self.rect = self.image.get_rect(center=coordinates)
        else:
            self.rect = self.image.get_rect(topleft=coordinates)
        self.no = no
        self.drawn = False
    
    def update(self): # Maybe optimize it!
        for no, tile_drawn in enumerate(drawn_tiles, 1):
            if self.no == no and self.drawn != tile_drawn:
                self.drawn_changer()

    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            self.drawn_changer()
            return True

    def drawn_changer(self, force_click=None):

        if force_click is None:
            self.drawn = not self.drawn
        elif force_click is True:
            self.drawn = True
        elif force_click is False:
            self.drawn = False

        if self.drawn:
            self.image.set_alpha(50)
            drawn_tiles[self.no-1] = 1
        else:
            self.image.set_alpha(255)
            drawn_tiles[self.no-1] = 0
        print(drawn_tiles)
   
def image_click_checker(group):
    for tile in group:
        collision = tile.check_click(event.pos)
        if collision:
            return True
    return False

pygame.init()
screen = pygame.display.set_mode(size=window_size)
pygame.display.set_caption('Bingo visualizer')
clock = pygame.time.Clock()

# Background
background_surface = pygame.image.load('graphics/background.png').convert()

# Plate
plate_center = (450, 450/2)
plate_image = pygame.image.load('graphics/plate.png').convert()
plate_image_rect = plate_image.get_rect(center=plate_center)

# Bingo_plate
plate_tile_group = pygame.sprite.Group()
box_distance = 78 + 5
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
plate_coordinates = [(plate_center[0] + box_distance*x, plate_center[1] + box_distance*y)
                      for y in [-1, 0, 1] for x in [-1, 0, 1]]
for no, coordinates in zip(numbers, plate_coordinates):
    plate_tile_group.add(Bingo_tile(no=no, coordinates=coordinates, plate=True))

# Bingo tiles
bingo_tile_group = pygame.sprite.Group()
tile_displace = (3, 135)
bingo_coordinates = [(tile_displace[0] + 45*x, tile_displace[1] + 45*y)
                      for y in range(7) for x in range(6)]
for no, coordinates in enumerate(bingo_coordinates):
    bingo_tile_group.add(Bingo_tile(no=no+1, coordinates=coordinates))

# Drawn tiles
drawn_tiles = [0] * 42

# Buttons
remove_all = pygame.image.load('graphics/remove_all.png').convert()
remove_all_rect = remove_all.get_rect(topleft=(3, 3))

direc_y = 175
horizontal = pygame.image.load('graphics/horizontal.png').convert()
horizontal_rect = horizontal.get_rect(center=(plate_center[0] - box_distance
                                            , plate_center[1]+direc_y))
vertical = pygame.image.load('graphics/vertical.png').convert()
vertical_rect = vertical.get_rect(center=(plate_center[0] 
                                            , plate_center[1]+direc_y))
full = pygame.image.load('graphics/full.png').convert()
full_rect = full.get_rect(center=(plate_center[0] + box_distance
                                            , plate_center[1]+direc_y))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if remove_all_rect.collidepoint(event.pos):
                for bingo_tile in bingo_tile_group:
                    bingo_tile.drawn_changer(force_click=False)
                for plate_tile in plate_tile_group:
                    plate_tile.drawn_changer(force_click=False)
            
            else:
                collision = False

                collision = image_click_checker(bingo_tile_group)

                if not collision:
                    image_click_checker(plate_tile_group)        

    # Background
    screen.blit(source=background_surface, dest=(0, 0))

    # Bingo tiles
    bingo_tile_group.draw(screen)

    # Plate
    screen.blit(plate_image, plate_image_rect)
    plate_tile_group.draw(screen)

    bingo_tile_group.update()
    plate_tile_group.update()

    # Buttons
    screen.blit(remove_all, remove_all_rect)
    screen.blit(horizontal, horizontal_rect)
    screen.blit(vertical, vertical_rect)
    screen.blit(full, full_rect)

    pygame.display.update()
    clock.tick(60)