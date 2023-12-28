import pygame

def bingo_mode_click_checker(game, mouse_pos):
    for no, button in enumerate(game.mode_rects, 1):
        if button.collidepoint(mouse_pos):
            return no
        
def bingo_mode_button_alpha(game, bingo_mode):
    h, v, f = 50, 50, 50

    if bingo_mode == 1:
        h = 255
    elif bingo_mode == 2:
        v = 255
    elif bingo_mode == 3:
        f = 255

    game.horizontal.set_alpha(h)
    game.vertical.set_alpha(v)
    game.full.set_alpha(f)

h_bingo = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
v_bingo = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
f_bingo = [[1, 2, 3, 4, 5, 6, 7, 8, 9]]
bingo_condition_types = [h_bingo, v_bingo, f_bingo]

def check_bingo(game):

    bingo = False

    # Surface to draw the lines
    game.line_surface = pygame.Surface(game.window_size, pygame.SRCALPHA)

    # If not looking for bingo
    if game.bingo_mode == 0:
        return False
    
    # See the tiles on the plate
    obtained = []
    for no, hat in enumerate(game.numbers, 1):
        if game.drawn_tiles[hat-1]:
            obtained.append(no)

    bingo_conditions = bingo_condition_types[game.bingo_mode-1]

    # Check with the conditions
    for line, bingo_condition in enumerate(bingo_conditions, -1):
        if set(bingo_condition).issubset(set(obtained)):
            bingo = True

            # Only draw lines for horizontal and vertical
            if game.bingo_mode in [1, 2]:
                draw_bingo_line(game=game, bingo_mode=game.bingo_mode, line=line)
        
    return bingo

def draw_bingo_line(game, bingo_mode, line):

    x, y = game.plate_center
    half_length = 1.5*game.box_distance

    if bingo_mode == 1:
        p0, p1 = (x - half_length, y + line*game.box_distance), (x + half_length, y + line*game.box_distance)
    elif bingo_mode == 2:
        p0, p1 = (x + line*game.box_distance, y - half_length), (x + line*game.box_distance, y + half_length)

    pygame.draw.line(game.line_surface, (255, 0, 0, 100), p0, p1, width=15)
