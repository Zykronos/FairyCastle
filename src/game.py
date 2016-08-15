import pygame as p 
import sys 
import os 
from tile import * 
from ui import * 
from player import * 
from goblin import * 

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
TRANS = (255, 0, 255) 
BLACK = (0, 0, 0) 
GREEN = (0, 255, 0) 

SCALE = 3 
TILE_DIMENSION = 16*SCALE 
VIEW_PORT = 20 
window_size = window_width, window_height = 1280, 960 
SCREEN_CENTER = (window_width//2, window_height//2) 
# Offsets the game board by a certain amount 
SCREEN_OFFSET_1 = (window_width//2-144, window_height//2-144) 
screen = p.display.set_mode(window_size) 
# Number of tiles in the game board 
board_size = board_width, board_height = 100, 100 
# The game board holds all non-actor tiles, such as the floor and walls 
game_board = [[0] * board_height for i in range(board_width)] 
# The actor board holds all player characters and enemies 
actor_board = [[0] * board_height for i in range(board_width)] 

# sprite loading will become increasing excessive as more sprites are added.  Need to figure out a way to clean this up in order to handle 100+ sprites.  Hopefully loading from sprite sheet will help 
sprites = dict(stoneWall=p.image.load(os.path.join('..', 'assets', 'environment', 'stoneWall.bmp')).convert(), 
            stoneWallHori=p.image.load(os.path.join('..', 'assets', 'environment', 'stoneWallHori.bmp')).convert(), 
            stoneWallVert=p.image.load(os.path.join('..', 'assets', 'environment', 'stoneWallVert.bmp')).convert(), 
            stoneWallCornerTL=p.image.load(os.path.join('..', 'assets', 'environment', 'stoneWallCornerTL.bmp')).convert(), 
            stoneWallCornerTR=p.image.load(os.path.join('..', 'assets', 'environment', 'stoneWallCornerTR.bmp')).convert(), 
            stoneWallCornerBL=p.image.load(os.path.join('..', 'assets', 'environment', 'stoneWallCornerBL.bmp')).convert(), 
            stoneWallCornerBR=p.image.load(os.path.join('..', 'assets', 'environment', 'stoneWallCornerBR.bmp')).convert(), 
            stoneFloor=p.image.load(os.path.join('..', 'assets', 'environment', 'stoneFloor.bmp')).convert(), 
            player=p.image.load(os.path.join('..', 'assets', 'actors', 'player.bmp')).convert(), 
            goblin=p.image.load(os.path.join('..', 'assets', 'actors', 'goblin.bmp')).convert(), 
            green_shirt=p.image.load(os.path.join('..', 'assets', 'actors', 'greenShirt.bmp')).convert(), 
            jester_hat=p.image.load(os.path.join('..', 'assets', 'actors', 'jesterHat.bmp')).convert(), 
            barb_outfit=p.image.load(os.path.join('..', 'assets', 'actors', 'barbarianOutfit.bmp')).convert(), 
            cursor=p.image.load(os.path.join('..', 'assets', '1/cursor.bmp')).convert())
# Goes through each sprite and sets a certain color to be transparent and scales it to the appropriate dimensions 
for i in sprites: 
    sprites[i].set_colorkey(TRANS) 
    sprites[i] = p.transform.scale(sprites[i], (TILE_DIMENSION, TILE_DIMENSION)) 

# vvvv Temp code for testing player drawing vvvv 
charPos = (75, 75)#(board_width//4, board_height//4) 
SCREEN_OFFSET = [SCREEN_CENTER[0]-charPos[0]*TILE_DIMENSION-4*TILE_DIMENSION, SCREEN_CENTER[1]-charPos[1]*TILE_DIMENSION] 
# ^^^^ Temp code for testing player drawing ^^^^ 
player = Player([sprites['player']], charPos, TILE_DIMENSION, SCREEN_OFFSET) 
#goblin = Goblin([sprites['goblin'], sprites['barb_outfit'], sprites['jester_hat']], (board_width//2, board_width//2), TILE_DIMENSION, SCREEN_OFFSET) 
ui = UI(window_size, board_size, 32, TILE_DIMENSION, SCREEN_OFFSET, sprites['cursor'])

def create_board(board_size): 
    ''' Creates the game board, initializing floor and wall tiles in game_board and players and enemies in actor_board '''
    for y in range(board_height): 
        for x in range(board_width): 
            if x == 0 and y == 0: 
                game_board[x][y] = Tile([sprites['stoneWallCornerTL']], (x, 
                y), TILE_DIMENSION, SCREEN_OFFSET, 'A wall', False) 
            elif x == board_width-1 and y == 0: 
                game_board[x][y] = Tile([sprites['stoneWallCornerTR']], (x, 
                y), TILE_DIMENSION, SCREEN_OFFSET, 'A wall', False) 
            elif x == 0 and y == board_height-1: 
                game_board[x][y] = Tile([sprites['stoneWallCornerBL']], (x, 
                y), TILE_DIMENSION, SCREEN_OFFSET, 'A wall', False) 
            elif x == board_width-1 and y == board_height-1: 
                game_board[x][y] = Tile([sprites['stoneWallCornerBR']], (x, 
                y), TILE_DIMENSION, SCREEN_OFFSET, 'A wall', False) 
            elif y == 0 or y == board_height-1: 
                game_board[x][y] = Tile([sprites['stoneWallHori']], (x, 
                y), TILE_DIMENSION, SCREEN_OFFSET, 'A wall', False) 
            elif x == 0 or x == board_width-1: 
                game_board[x][y] = Tile([sprites['stoneWallVert']], (x, 
                y), TILE_DIMENSION, SCREEN_OFFSET, 'A wall', False)
            elif x == 0 or x == board_width-1 or y == 0 or y == board_height-1: 
                game_board[x][y] = Tile([sprites['stoneWall']], (x, 
                y), TILE_DIMENSION, SCREEN_OFFSET, 'A wall', False) 
            else: 
                game_board[x][y] = Tile([sprites['stoneFloor']], (x, y), TILE_DIMENSION, SCREEN_OFFSET, 'The floor') 
    actor_board[player.pos_index[0]][player.pos_index[1]] = player 
    
    
def draw_board(VIEW_PORT): 
    if player.pos_index[0]+VIEW_PORT//2+1<=board_width and player.pos_index[1]+VIEW_PORT//2+1<=board_height: 
        for y in range(player.pos_index[1]-VIEW_PORT//2, player.pos_index[1]+VIEW_PORT//2+1): 
            for x in range(player.pos_index[0]-VIEW_PORT//2, player.pos_index[0]+VIEW_PORT//2+1): 
                can_draw(game_board[x][y]) 
                can_draw(actor_board[x][y]) 
    elif player.pos_index[0]+VIEW_PORT//2+1>board_width and player.pos_index[1]+VIEW_PORT//2+1<=board_height: 
        for y in range(player.pos_index[1]-VIEW_PORT//2, player.pos_index[1]+VIEW_PORT//2+1): 
            for x in range(player.pos_index[0]-VIEW_PORT//2, board_width): 
                can_draw(game_board[x][y]) 
                can_draw(actor_board[x][y]) 
    elif player.pos_index[1]+VIEW_PORT//2+1>board_height and player.pos_index[0]+VIEW_PORT//2+1<=board_width: 
        for y in range(player.pos_index[1]-VIEW_PORT//2, board_height): 
            for x in range(player.pos_index[0]-VIEW_PORT//2, player.pos_index[0]+VIEW_PORT//2+1): 
                can_draw(game_board[x][y]) 
                can_draw(actor_board[x][y]) 
    else: 
        for y in range(player.pos_index[1]-VIEW_PORT//2, board_height): 
            for x in range(player.pos_index[0]-VIEW_PORT//2, board_width): 
                can_draw(game_board[x][y]) 
                can_draw(actor_board[x][y]) 

def can_draw(tile): 
    ''' Checks to see if an index in either game_board or actor_board is an actual tile, then displays it if it's within screen bounds '''
    if type(tile) != int: 
        temp = tile 
        temp.move(SCREEN_OFFSET)
        if (temp.pos_coordinates[0] < ui.edge[0][0] and temp.pos_coordinates[0] >= -TILE_DIMENSION and temp.pos_coordinates[1] >= 0 and temp.pos_coordinates[1] < window_height): 
                tile.move(SCREEN_OFFSET) 
                tile.render(screen) 
        else: 
            tile.render(screen) 

def can_move(tile, direction): 
    # Need to rework this function to handle movement checking more elegantly 
    if  direction == 'up': 
        if type(actor_board[tile.pos_index[0]][tile.pos_index[1] - 1]) != int: 
            return game_board[tile.pos_index[0]][tile.pos_index[1] - 1].is_walkable and actor_board[tile.pos_index[0]][tile.pos_index[1] - 1].is_walkable 
        else: 
            return game_board[tile.pos_index[0]][tile.pos_index[1] - 1].is_walkable 
    if  direction == 'down': 
        return  game_board[tile.pos_index[0]][tile.pos_index[1] + 1].is_walkable 
    if  direction == 'left': 
        return  game_board[tile.pos_index[0] - 1][tile.pos_index[1]].is_walkable 
    if  direction == 'right': 
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
    ui.update(clock) 
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
    
create_board(board_size) 
clock = p.time.Clock() 
done = False 
while not done: 
    direction = input() 
    update(direction, clock) 
    render() 
    clock.tick(60) 

p.quit() 