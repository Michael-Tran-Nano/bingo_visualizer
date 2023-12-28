import pygame
from sys import exit

from scripts.tiles import Tiles, Plate_tiles, tile_collision_checker
from scripts.bingo_checker import bingo_mode_click_checker, bingo_mode_button_alpha, check_bingo

class Game:
    def __init__(self):
        pygame.init()

        self.window_size = (900, 450)

        pygame.display.set_caption(title='Bingo simulator')
        self.screen = pygame.display.set_mode(size=self.window_size)

        self.clock = pygame.time.Clock()

        # Background
        self.background = pygame.image.load('graphics/background.png').convert()

        # Tiles
        self.tile_group = pygame.sprite.Group()
        tile_displace = (3, 135)
        bingo_coordinates = [(tile_displace[0] + 45*x, tile_displace[1] + 45*y)
                      for y in range(7) for x in range(6)]
        for no, coordinates in enumerate(bingo_coordinates, 1):
            self.tile_group.add(Tiles(game=self, no=no, coordinates=coordinates))

        # Plate
        self.plate_center = (450, 450/2)
        self.plate_image = pygame.image.load('graphics/plate.png').convert()
        self.plate_image_rect = self.plate_image.get_rect(center=self.plate_center)

        # Bingo_plate
        self.plate_tile_group = pygame.sprite.Group()
        self.box_distance = 78 + 5
        self.numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        plate_coordinates = [(self.plate_center[0] + self.box_distance*x, self.plate_center[1] + self.box_distance*y)
                             for y in [-1, 0, 1] for x in [-1, 0, 1]]
        for no, coordinates in zip(self.numbers, plate_coordinates):
            self.plate_tile_group.add(Plate_tiles(game=self, no=no, coordinates=coordinates))

        # Drawn tiles
        self.drawn_tiles = [False] * 42

        # Remove all
        self.remove_all = pygame.image.load('graphics/remove_all.png').convert()
        self.remove_all_rect = self.remove_all.get_rect(topleft=(3, 3))

        # Mode buttons
        direc_y = 175
        self.horizontal = pygame.image.load('graphics/horizontal.png').convert()
        self.horizontal_rect = self.horizontal.get_rect(center=(self.plate_center[0] - self.box_distance, 
                                                                self.plate_center[1] + direc_y))
        self.vertical = pygame.image.load('graphics/vertical.png').convert()
        self.vertical_rect = self.vertical.get_rect(center=(self.plate_center[0],
                                                            self.plate_center[1] + direc_y))
        self.full = pygame.image.load('graphics/full.png').convert()
        self.full_rect = self.full.get_rect(center=(self.plate_center[0] + self.box_distance,
                                                    self.plate_center[1] + direc_y))
        self.mode_images = [self.horizontal, self.vertical, self.full]
        self.mode_rects = [self.horizontal_rect, self.vertical_rect, self.full_rect]

        # Bingo mode
        self.horizontal.set_alpha(50)
        self.vertical.set_alpha(50)
        self.full.set_alpha(50)
        self.bingo_mode = 0
        self.bingo_now = False
        self.line_surface = pygame.Surface(self.window_size, pygame.SRCALPHA) 

        # Bingo graphic
        self.bingo_graphic = pygame.image.load('graphics/bingo.png').convert_alpha()
        self.bingo_graphic_rect = self.bingo_graphic.get_rect(center=self.plate_center)
    
    def run(self):

        while True:

            # Background
            self.screen.blit(self.background, dest=(0, 0))

            # Bingo tiles
            self.tile_group.draw(self.screen)

            # Plate
            self.screen.blit(self.plate_image, self.plate_image_rect)
            self.plate_tile_group.draw(self.screen)

            # Buttons
            self.screen.blit(self.remove_all, self.remove_all_rect)
            self.screen.blit(self.horizontal, self.horizontal_rect)
            self.screen.blit(self.vertical, self.vertical_rect)
            self.screen.blit(self.full, self.full_rect)

            if self.bingo_now:
                self.screen.blit(self.line_surface, (0, 0))
                self.screen.blit(self.bingo_graphic, self.bingo_graphic_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    # Remove all?
                    if self.remove_all_rect.collidepoint(event.pos):
                        self.drawn_tiles = [False] * 42
                        self.tile_group.update()
                        self.plate_tile_group.update()
                        self.bingo_now = check_bingo(self)
                        break
                    
                    # Clicked on tile?
                    clicked_no = (tile_collision_checker(tile_group=self.tile_group,
                                                        mouse_pos=event.pos)
                                  or
                                  tile_collision_checker(tile_group=self.plate_tile_group,
                                                        mouse_pos=event.pos))
                    if clicked_no:
                        self.drawn_tiles[clicked_no-1] = not self.drawn_tiles[clicked_no-1]
                        self.tile_group.update()
                        self.plate_tile_group.update()
                        self.bingo_now = check_bingo(self)
                        break
                        
                    # Change mode?
                    clicked_mode = bingo_mode_click_checker(game=self, mouse_pos=event.pos)
                    if clicked_mode:
                        self.bingo_mode = clicked_mode if (self.bingo_mode != clicked_mode) else 0
                        bingo_mode_button_alpha(game=self, bingo_mode=self.bingo_mode)
                        self.bingo_now = check_bingo(self)
                        break

            pygame.display.update()
            self.clock.tick(60)

Game().run()