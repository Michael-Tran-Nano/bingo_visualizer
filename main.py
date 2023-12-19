import pygame
from sys import exit

# Settings
window_size = (900, 450)

class Bingo_tile(pygame.sprite.Sprite):

    def __init__(self, no, coordinates, plate=False):
        super().__init__()

        self.image = pygame.image.load(f'tiles/{no}.png').convert()

        # On the bingo plate
        if plate:
            self.rect = self.image.get_rect(center=coordinates)
        # Click-able tiles on the left
        else:
            self.rect = self.image.get_rect(topleft=coordinates)

        self.no = no
        self.drawn = False
    
    # Check if you have clicked on a tile
    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            self.drawn_changer()
            return True

    # Check if the clicked tile is both on the left and the plate
    def update(self):
        for no, tile_drawn in enumerate(drawn_tiles, 1):
            if self.no == no and self.drawn != tile_drawn:
                self.drawn_changer() 

    def drawn_changer(self, force_click=None):

        if force_click is None:
            self.drawn = not self.drawn
        
        # When you want to flip them all
        elif force_click is True:
            self.drawn = True
        elif force_click is False:
            self.drawn = False

        self.change_tile_visibility()

    def change_tile_visibility(self):
        if self.drawn:
            self.image.set_alpha(50)
            drawn_tiles[self.no-1] = 1
        else:
            self.image.set_alpha(255)
            drawn_tiles[self.no-1] = 0
   
def tile_click_checker(group):
    for tile in group:
        collision = tile.check_click(event.pos)
        if collision:
            return True
    return False

def bingo_mode_click_checker():
    for no, button in enumerate(mode_rects, 1):
        if button.collidepoint(event.pos):
            return no

def bingo_mode_button_alpha(bingo_mode):
    h, v, f = 50, 50, 50

    if bingo_mode == 1:
        h = 255
    elif bingo_mode == 2:
        v = 255
    elif bingo_mode == 3:
        f = 255

    horizontal.set_alpha(h)
    vertical.set_alpha(v)
    full.set_alpha(f)

def check_bingo():

    bingo = False
    
    # Surface to draw the lines
    line_surface = pygame.Surface(window_size, pygame.SRCALPHA) 

    # If not looking for bingo
    if bingo_mode == 0:
        return False, line_surface

    obtained = []
    for no, hat in enumerate(numbers, 1):
        if drawn_tiles[hat-1]:
            obtained.append(no)
    
    bingo_conditions = bingo_condition_types[bingo_mode-1]

    for line, bingo_condition in enumerate(bingo_conditions, -1):
        if set(bingo_condition).issubset(set(obtained)):
            bingo = True

            # Only draw lines for horizontal and vertical
            if bingo_mode in [1, 2]:
                draw_bingo_line(bingo_mode, line, line_surface)
        
    return bingo, line_surface

def draw_bingo_line(bingo_mode, line, line_surface):

    x, y = plate_center
    half_length = 1.5*box_distance

    if bingo_mode == 1:
        p0, p1 = (x - half_length, y + line*box_distance), (x + half_length, y + line*box_distance)
    elif bingo_mode == 2:
        p0, p1 = (x + line*box_distance, y - half_length),(x + line*box_distance, y + half_length)

    pygame.draw.line(line_surface, (255, 0, 0, 100), p0, p1, width=15)
    return line_surface

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

# Bingo tiles (left side)
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

# Mode buttons
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
mode_images = [horizontal, vertical, full]
mode_rects = [horizontal_rect, vertical_rect, full_rect]

# Bingo mode
horizontal.set_alpha(50)
vertical.set_alpha(50)
full.set_alpha(50)
bingo_mode = 0
h_bingo = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
v_bingo = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
f_bingo = [[1, 2, 3, 4, 5, 6, 7, 8, 9]]
bingo_condition_types = [h_bingo, v_bingo, f_bingo]
bingo_now = False
line_surface = pygame.Surface(window_size, pygame.SRCALPHA) 

# Bingo graphic
bingo_graphic = pygame.image.load('graphics/bingo.png').convert_alpha()
bingo_graphic_rect = bingo_graphic.get_rect(center=plate_center)

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
                tile_collision = (tile_click_checker(bingo_tile_group) 
                                  or tile_click_checker(plate_tile_group))

                if tile_collision:
                    bingo_tile_group.update()
                    plate_tile_group.update()
                    if bingo_mode != 0:
                        bingo_now, line_surface = check_bingo()

                # Check for change in mode
                else:
                    mode_number = bingo_mode_click_checker()

                    # If any mode button is clicked
                    if mode_number:
                        bingo_mode = mode_number if (mode_number != bingo_mode) else 0
                        bingo_mode_button_alpha(bingo_mode)
                        bingo_now, line_surface = check_bingo()
                
                

    # Background
    screen.blit(source=background_surface, dest=(0, 0))

    # Bingo tiles
    bingo_tile_group.draw(screen)

    # Plate
    screen.blit(plate_image, plate_image_rect)
    plate_tile_group.draw(screen)

    # Buttons
    screen.blit(remove_all, remove_all_rect)
    screen.blit(horizontal, horizontal_rect)
    screen.blit(vertical, vertical_rect)
    screen.blit(full, full_rect)

    # Bingo lines
    if bingo_now:
        screen.blit(line_surface, (0, 0))
        screen.blit(bingo_graphic, bingo_graphic_rect)

    pygame.display.update()
    clock.tick(60)