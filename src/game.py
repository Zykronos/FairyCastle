import pygame as p 
import sys 
import os 
from tile import * 
from ui import * 
from player import * 
from goblin import * 
from spriteLoader import * 
from levelLoader import * 

p.init() 
p.display.set_caption('Fairy Castle') 

''' TODO ''' 
# Add comments 
# Implement level reader to load levels from external text files 
# Implement Sprite() class to manage sprite loading (e.g. loading sprites from sprite sheets) 
# Make code cleaner 
# Reconsider having game_board and actor_board be separate 
# Add heartbeat code 

''' Colors ''' 
TRANS = (128, 0, 128) 
BLACK = (0, 0, 0) 
GREEN = (0, 255, 0) 

SCALE = 3 
TILE_DIMENSION = 16*SCALE 
VIEW_PORT = 20 
window_size = window_width, window_height = 1280, 960 
SCREEN_CENTER = (window_width//2, window_height//2) 
screen = p.display.set_mode(window_size) 
# Number of tiles in the game board 
board_size = board_width, board_height = 20, 20 
# The game board holds all non-actor tiles, such as the floor and walls 
game_board = [[0] * board_height for i in range(board_width)] 
# The actor board holds all player characters and enemies 
actor_board = [[0] * board_height for i in range(board_width)] 
sprites = dict(actorSheet=p.image.load(os.path.join('..', 'assets', 'spriteSheets', 'actorSpriteSheet6x6.png')).convert(), 
            environmentSheet=p.image.load(os.path.join('..', 'assets', 'spriteSheets', 'environmentSpriteSheet15x8.png')).convert(), 
            itemSheet=p.image.load(os.path.join('..', 'assets', 'spriteSheets', 'itemSpriteSheet6x6.png')).convert()) 
levels = dict(level_t=os.path.join('..', 'levels', 'level_t.txt')) 
# Goes through each sprite and sets a certain color to be transparent and scales it to the appropriate dimensions 
for i in sprites: 
    sprites[i].set_colorkey(TRANS) 
    
# Splits the sprite sheet into individual sprites and adds them to t.  Indices of t correlate to positions in the sprite sheet 
actor_sprite_sheet = [[0] * 6 for x in range(6)]
sprite_loader = Sprite(sprites['actorSheet'], (0, 0), 16, 1, 6, 6) 
for y in range(6): 
    for x in range(6): 
        actor_sprite_sheet[x][y] = sprite_loader.sprite(x, y) 
        actor_sprite_sheet[x][y] = p.transform.scale(actor_sprite_sheet[x][y], (TILE_DIMENSION, TILE_DIMENSION)) 
environment_sprite_sheet = [[0] * 8 for x in range(15)]
sprite_loader = Sprite(sprites['environmentSheet'], (0, 0), 16, 1, 15, 8) 
for y in range(8): 
    for x in range(15): 
        environment_sprite_sheet[x][y] = sprite_loader.sprite(x, y) 
        environment_sprite_sheet[x][y] = p.transform.scale(environment_sprite_sheet[x][y], (TILE_DIMENSION, TILE_DIMENSION)) 
item_sprite_sheet = [[0] * 6 for x in range(6)]
sprite_loader = Sprite(sprites['itemSheet'], (0, 0), 16, 1, 6, 6) 
for y in range(6): 
    for x in range(6): 
        item_sprite_sheet[x][y] = sprite_loader.sprite(x, y) 
        item_sprite_sheet[x][y] = p.transform.scale(item_sprite_sheet[x][y], (TILE_DIMENSION, TILE_DIMENSION)) 

level = LevelLoader(levels['level_t'], window_size, actor_sprite_sheet, environment_sprite_sheet, item_sprite_sheet) 
level.load(TILE_DIMENSION) 
player = level.player 
game_board = level.game_board 
actor_board = level.actor_board 
board_width = level.board_width 
board_height = level.board_height 
enemies = level.enemies 
# Subtracting 4*TILE_DIMENSION to move the player to the center of the playable window rather than the entire window.  Don't know where the 32 comes from 
# Offsets the game board by a certain amount 
SCREEN_OFFSET = [SCREEN_CENTER[0]-player.pos_index[0]*TILE_DIMENSION-4*TILE_DIMENSION+32, SCREEN_CENTER[1]-player.pos_index[1]*TILE_DIMENSION] 
player.pos_coordinates = SCREEN_OFFSET 
ui = UI(window_size, board_size, 32, TILE_DIMENSION, SCREEN_OFFSET, actor_sprite_sheet[0][1])

def create_board1(board_size): 
    ''' Creates the game board, initializing floor and wall tiles in game_board and players and enemies in actor_board '''
    for y in range(board_height): 
        for x in range(board_width): 
            if x == 0 and y == 0: # top left 
                game_board[x][y] = Tile([t[2][7]], (x, 
                y), TILE_DIMENSION, SCREEN_OFFSET, 'A wall', False) 
            elif x == board_width-1 and y == 0: # top right 
                game_board[x][y] = Tile([t[3][7]], (x, 
                y), TILE_DIMENSION, SCREEN_OFFSET, 'A wall', False) 
            elif x == 0 and y == board_height-1: # bottom left 
                game_board[x][y] = Tile([t[5][7]], (x, 
                y), TILE_DIMENSION, SCREEN_OFFSET, 'A wall', False) 
            elif x == board_width-1 and y == board_height-1: # bottom right 
                game_board[x][y] = Tile([t[4][7]], (x, 
                y), TILE_DIMENSION, SCREEN_OFFSET, 'A wall', False) 
            elif y == 0 or y == board_height-1: # horizontal wall 
                game_board[x][y] = Tile([t[1][7]], (x, 
                y), TILE_DIMENSION, SCREEN_OFFSET, 'A wall', False) 
            elif x == 0 or x == board_width-1: # vertical wall 
                game_board[x][y] = Tile([t[0][7]], (x, 
                y), TILE_DIMENSION, SCREEN_OFFSET, 'A wall', False)
            else: # floor 
                game_board[x][y] = Tile([t[8][8]], (x, y), TILE_DIMENSION, SCREEN_OFFSET, 'The floor') 
    actor_board[player.pos_index[0]][player.pos_index[1]] = player 
    
def create_board(board_width, board_height): 
    for y in range(board_height): 
        for x in range(board_width): 
            if type(game_board[x][y]) != int: 
                game_board[x][y].update(SCREEN_OFFSET) 
            if type(actor_board[x][y]) != int: 
                actor_board[x][y].update(SCREEN_OFFSET) 

def draw_board(VIEW_PORT): 
    if player.pos_index[0]+VIEW_PORT//2+1<=board_width and player.pos_index[1]+VIEW_PORT//2+1<=board_height: 
        for y in range(player.pos_index[1]-VIEW_PORT//2, player.pos_index[1]+VIEW_PORT//2+1): 
            for x in range(player.pos_index[0]-VIEW_PORT//2, player.pos_index[0]+VIEW_PORT//2+1): 
                if type(game_board[x][y]) != int: 
                    game_board[x][y].update(SCREEN_OFFSET) 
                    can_draw(game_board[x][y]) 
                if type(actor_board[x][y]) != int: 
                    actor_board[x][y].update(SCREEN_OFFSET) 
                    can_draw(actor_board[x][y]) 
    elif player.pos_index[0]+VIEW_PORT//2+1>board_width and player.pos_index[1]+VIEW_PORT//2+1<=board_height: 
        for y in range(player.pos_index[1]-VIEW_PORT//2, player.pos_index[1]+VIEW_PORT//2+1): 
            for x in range(player.pos_index[0]-VIEW_PORT//2, board_width): 
                if type(game_board[x][y]) != int: 
                    game_board[x][y].update(SCREEN_OFFSET) 
                    can_draw(game_board[x][y]) 
                if type(actor_board[x][y]) != int: 
                    actor_board[x][y].update(SCREEN_OFFSET) 
                    can_draw(actor_board[x][y]) 
    elif player.pos_index[1]+VIEW_PORT//2+1>board_height and player.pos_index[0]+VIEW_PORT//2+1<=board_width: 
        for y in range(player.pos_index[1]-VIEW_PORT//2, board_height): 
            for x in range(player.pos_index[0]-VIEW_PORT//2, player.pos_index[0]+VIEW_PORT//2+1): 
                if type(game_board[x][y]) != int: 
                    game_board[x][y].update(SCREEN_OFFSET) 
                    can_draw(game_board[x][y]) 
                if type(actor_board[x][y]) != int: 
                    actor_board[x][y].update(SCREEN_OFFSET) 
                    can_draw(actor_board[x][y]) 
    else: 
        for y in range(player.pos_index[1]-VIEW_PORT//2, board_height): 
            for x in range(player.pos_index[0]-VIEW_PORT//2, board_width): 
                if type(game_board[x][y]) != int: 
                    game_board[x][y].update(SCREEN_OFFSET) 
                    can_draw(game_board[x][y]) 
                if type(actor_board[x][y]) != int: 
                    actor_board[x][y].update(SCREEN_OFFSET) 
                    can_draw(actor_board[x][y]) 

def can_draw(tile): 
    ''' Checks to see if an index in either game_board or actor_board is an actual tile, then displays it if it's within screen bounds '''
    if type(tile) != int: 
        if (tile.pos_coordinates[0] < ui.edge[0][0] and tile.pos_coordinates[0] >= -TILE_DIMENSION and tile.pos_coordinates[1] >= 0 and tile.pos_coordinates[1] < window_height): 
                tile.render(screen) 
        
def can_move(tile, direction): 
    # Need to rework this function to handle movement checking more elegantly 
    if  direction == 'up': 
        if type(actor_board[tile.pos_index[0]][tile.pos_index[1] - 1]) != int: 
            return game_board[tile.pos_index[0]][tile.pos_index[1] - 1].is_walkable and actor_board[tile.pos_index[0]][tile.pos_index[1] - 1].is_walkable 
        else: 
            return game_board[tile.pos_index[0]][tile.pos_index[1] - 1].is_walkable 
    if  direction == 'down': 
        if type(actor_board[tile.pos_index[0]][tile.pos_index[1] + 1]) != int: 
            return game_board[tile.pos_index[0]][tile.pos_index[1] + 1].is_walkable and actor_board[tile.pos_index[0]][tile.pos_index[1] + 1].is_walkable 
        else: 
            return  game_board[tile.pos_index[0]][tile.pos_index[1] + 1].is_walkable 
    if  direction == 'left': 
        if type(actor_board[tile.pos_index[0] - 1][tile.pos_index[1]]) != int: 
            return game_board[tile.pos_index[0] - 1][tile.pos_index[1]].is_walkable and actor_board[tile.pos_index[0] - 1][tile.pos_index[1]].is_walkable 
        else: 
            return  game_board[tile.pos_index[0] - 1][tile.pos_index[1]].is_walkable 
    if  direction == 'right': 
        if type(actor_board[tile.pos_index[0] + 1][tile.pos_index[1]]) != int: 
            return game_board[tile.pos_index[0] + 1][tile.pos_index[1]].is_walkable and actor_board[tile.pos_index[0] + 1][tile.pos_index[1]].is_walkable 
        else: 
            return  game_board[tile.pos_index[0] + 1][tile.pos_index[1]].is_walkable 
    
def move_board(direction): 
    global SCREEN_OFFSET 
    if  direction == 'up': 
        SCREEN_OFFSET[1] += TILE_DIMENSION 
    if  direction == 'down': 
        SCREEN_OFFSET[1] -= TILE_DIMENSION
    if  direction == 'left': 
        SCREEN_OFFSET[0] += TILE_DIMENSION
    if  direction == 'right': 
        SCREEN_OFFSET[0] -= TILE_DIMENSION 
    
def input(): 
    direction = '' 
    p.event.pump() 
    for e in p.event.get(): 
        if e.type == p.QUIT: 
            sys.exit() 
        if e.type == p.KEYDOWN: 
            if e.key == p.K_ESCAPE: 
                sys.exit() 
            if e.key == p.K_UP: 
                direction = 'up' 
            if e.key == p.K_DOWN: 
                direction = 'down' 
            if e.key == p.K_LEFT: 
                direction = 'left' 
            if e.key == p.K_RIGHT: 
                direction = 'right' 
    return direction 

def update(direction, clock): 
    ui.update(clock, SCREEN_OFFSET) 
    actor_board[player.pos_index[0]][player.pos_index[1]] = 0 
    if can_move(player, direction): 
        player.move(direction) 
        move_board(direction) 
    actor_board[player.pos_index[0]][player.pos_index[1]] = player 
    
def render(): 
    screen.fill(BLACK) 
    draw_board(VIEW_PORT) 
    ui.render(screen, GREEN, game_board, actor_board) 
    p.display.flip() 
    
create_board(board_width, board_height) 
clock = p.time.Clock() 
done = False 
while not done: 
    direction = input() 
    update(direction, clock) 
    render() 
    clock.tick(60) 

p.quit() 