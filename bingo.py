import pygame
from sys import exit

from scripts.tiles import Tiles, Plate_tiles, tile_collision_checker
from scripts.bingo_checker import bingo_mode_click_checker, bingo_mode_button_alpha, check_bingo
from scripts.input_checker import input_checker

class Game:
    def __init__(self):
        pygame.init()

        self.window_size = (900, 450)

        pygame.display.set_caption(title='Bingo simulator')
        self.screen = pygame.display.set_mode(size=self.window_size)

        self.clock = pygame.time.Clock()

        # Background
        self.background = pygame.image.load('graphics/background.png').convert()

        # Title
        self.title = pygame.image.load('graphics/title.png').convert_alpha()
        self.title_rect = self.title.get_rect(midtop=(450, 15))

        # Tiles
        self.tile_group = pygame.sprite.Group()
        tile_displace = (30, 30)
        bingo_coordinates = [(tile_displace[0] + 45*x, tile_displace[1] + 45*y)
                             for y in range(7) for x in range(6)]
        for no, coordinates in enumerate(bingo_coordinates, 1):
            self.tile_group.add(Tiles(game=self, no=no, coordinates=coordinates))

        # Drawn tiles
        self.drawn_tiles = [False] * 42

        # Plate
        self.plate_center = (450, 450/2)
        self.plate_image = pygame.image.load('graphics/plate.png').convert()
        self.plate_image_rect = self.plate_image.get_rect(center=self.plate_center)

        # Bingo_plate_tiles
        self.numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.new_plate(self.numbers)        

        # buttons
        self.remove_all = pygame.image.load('graphics/remove_all.png').convert()
        self.remove_all_rect = self.remove_all.get_rect(bottomleft=(3, self.window_size[1] - 3))
        self.change_plate = pygame.image.load('graphics/change_plate.png').convert()
        self.change_plate_rect = self.change_plate.get_rect(topleft=(3, 370))
        self.clear_box = pygame.image.load('graphics/clear_box.png').convert()
        self.clear_box_rect = self.clear_box.get_rect(topleft=(50 + 220 + 3, 370))

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

        # Textbox
        self.base_font = pygame.font.Font(None, 24)
        self.base_font_small = pygame.font.Font(None, 16) 
        self.user_text = ''
        self.input_rect = pygame.Rect(48, 370, 140, 24)
        self.text_box_active = False
        self.blinker = 0.0
        self.error_message = ''

    def new_plate(self, numbers):
        self.plate_tile_group = pygame.sprite.Group()
        self.box_distance = 78 + 5
        self.numbers = numbers
        plate_coordinates = [(self.plate_center[0] + self.box_distance*x, self.plate_center[1] + self.box_distance*y)
                             for y in [-1, 0, 1] for x in [-1, 0, 1]]
        for no, coordinates in zip(self.numbers, plate_coordinates):
            self.plate_tile_group.add(Plate_tiles(game=self, no=no, coordinates=coordinates))
    
    def run(self):

        while True:

            # Background
            self.screen.blit(self.background, dest=(0, 0))

            # Title
            self.screen.blit(self.title, self.title_rect)

            # Bingo tiles
            self.tile_group.draw(self.screen)

            # Plate
            self.screen.blit(self.plate_image, self.plate_image_rect)
            self.plate_tile_group.draw(self.screen)

            # Textbox
            if self.text_box_active:
                self.blinker += 0.02
                screen_text = self.user_text + ('|' if int(self.blinker) % 2 else '')
                self.box_color = (255, 255, 255)
            else:
                screen_text = self.user_text if self.user_text else "Write bingo numbers here"
                self.box_color = (155, 155, 155)

            pygame.draw.rect(self.screen, self.box_color, self.input_rect)
            text_surface = self.base_font.render(screen_text, True, (0, 0, 0))
            self.screen.blit(text_surface, (self.input_rect.x+5, self.input_rect.y+5))
            self.input_rect.w = max(220, text_surface.get_width()+10)
            text_surface_error = self.base_font_small.render(self.error_message, True, (255, 0, 0))
            self.screen.blit(text_surface_error, (self.input_rect.x + 5, self.input_rect.y+25))

            # Buttons
            self.screen.blit(self.remove_all, self.remove_all_rect)
            self.screen.blit(self.change_plate, self.change_plate_rect)
            self.screen.blit(self.clear_box, self.clear_box_rect)
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
                    
                    # Clicked on text box?
                    if self.input_rect.collidepoint(event.pos):
                        self.text_box_active = True
                        break
                    else:
                        self.text_box_active = False
                        self.error_message = ''

                    # Change plate?
                    if self.change_plate_rect.collidepoint(event.pos):
                        self.text_box_active = True
                        numbers, message = input_checker(self.user_text)
                        self.error_message = message
                        if numbers:
                            self.new_plate(numbers)
                            self.plate_tile_group.update()
                            self.bingo_now = check_bingo(self)
                        break

                    # Clear box?a
                    if self.clear_box_rect.collidepoint(event.pos):
                        self.text_box_active = True
                        self.user_text = ''
                        break

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

                if event.type == pygame.KEYDOWN and self.text_box_active: 
                    if event.key == pygame.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    else:
                        key = event.unicode
                        if key.isnumeric() or key == ' ':
                            self.user_text += key

            pygame.display.update()
            self.clock.tick(60)

Game().run()