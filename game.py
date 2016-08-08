import pygame as p 
import sys 
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
# Change character movement to scroll map rather than move player 

''' Colors ''' 
TRANS = (255, 0, 255) 
BLACK = (0, 0, 0) 
GREEN = (0, 255, 0) 

SCALE = 3 
TILE_DIMENSION = 16*SCALE 
window_size = window_width, window_height = 1280, 960 
# Offsets the game board by a certain amount 
SCREEN_OFFSET = (100, 100) #(window_width//2, window_height//2) 
screen = p.display.set_mode(window_size) 
# Number of tiles in the game board 
board_size = board_width, board_height = 15, 10 
# The game board holds all non-actor tiles, such as the floor and walls 
game_board = [[0] * board_height for i in range(board_width)] 
# The actor board holds all player characters and enemies 
actor_board = [[0] * board_height for i in range(board_width)] 

# sprite loading will become increasing excessive as more sprites are added.  Need to figure out a way to clean this up in order to handle 100+ sprites.  Hopefully loading from sprite sheet will help 
sprites = dict(stoneWall=p.image.load('assets/stoneWall.bmp').convert(), 
            stoneWallHori=p.image.load('assets/stoneWallHori.bmp').convert(), 
            stoneWallVert=p.image.load('assets/stoneWallVert.bmp').convert(), 
            stoneWallCornerTL=p.image.load('assets/stoneWallCornerTL.bmp').convert(), 
            stoneWallCornerTR=p.image.load('assets/stoneWallCornerTR.bmp').convert(), 
            stoneWallCornerBL=p.image.load('assets/stoneWallCornerBL.bmp').convert(), 
            stoneWallCornerBR=p.image.load('assets/stoneWallCornerBR.bmp').convert(), 
            stoneFloor=p.image.load('assets/stoneFloor.bmp').convert(), 
            player=p.image.load('assets/player.bmp').convert(), 
            goblin=p.image.load('assets/goblin.bmp').convert(), 
            green_shirt=p.image.load('assets/greenShirt.bmp').convert(), 
            jester_hat=p.image.load('assets/jesterHat.bmp').convert(), 
            barb_outfit=p.image.load('assets/barbarianOutfit.bmp').convert(), 
            cursor=p.image.load('assets/1/cursor.bmp').convert())
# Goes through each sprite and sets a certain color to be transparent and scales it to the appropriate dimensions 
for i in sprites: 
    sprites[i].set_colorkey(TRANS) 
    sprites[i] = p.transform.scale(sprites[i], (TILE_DIMENSION, TILE_DIMENSION)) 

player = Player([sprites['player']], (board_width//4, board_width//4), TILE_DIMENSION, SCREEN_OFFSET) 
goblin = Goblin([sprites['goblin'], sprites['barb_outfit'], sprites['jester_hat']], (board_width//2, board_width//2), TILE_DIMENSION, SCREEN_OFFSET) 
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
    actor_board[goblin.pos_index[0]][goblin.pos_index[1]] = goblin 

def draw_board(board_size): 
    for y in range(board_size[1]): 
        for x in range(board_size[0]): 
            can_draw(game_board[x][y]) 
            can_draw(actor_board[x][y]) 

def can_draw(tile): 
    ''' Checks to see if an index in either game_board or actor_board is an actual tile, then displays it if it's within screen bounds '''
    if type(tile) != int and tile.pos_coordinates[0] < ui.edge[0][0]: 
        tile.render(screen) 
    
def can_move(tile, direction): 
    if  direction == 'up': 
        return game_board[tile.pos_index[0]][tile.pos_index[1] - 1].is_walkable 
    if  direction == 'down': 
        return game_board[tile.pos_index[0]][tile.pos_index[1] + 1].is_walkable 
    if  direction == 'left': 
        return game_board[tile.pos_index[0] - 1][tile.pos_index[1]].is_walkable 
    if  direction == 'right': 
        return game_board[tile.pos_index[0] + 1][tile.pos_index[1]].is_walkable 

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

def update(direction): 
    ui.update() 
    actor_board[player.pos_index[0]][player.pos_index[1]] = 0 
    if can_move(player, direction): 
        player.move(direction) 
    create_board(board_size) 


def render(): 
    screen.fill(BLACK) 
    draw_board(board_size) 
    ui.render(screen, GREEN, game_board, actor_board) 
    p.display.flip() 
    
clock = p.time.Clock() 
done = False 
while not done: 
    direction = input() 
    update(direction) 
    render() 
    clock.tick(60) 

p.quit() 