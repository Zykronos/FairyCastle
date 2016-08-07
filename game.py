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
# Implement character movement 

''' Colors ''' 
TRANS = (255, 0, 255) 
BLACK = (0, 0, 0) 
GREEN = (0, 255, 0) 

SCALE = 3 
TILE_DIMENSION = 16*SCALE 
window_size = window_width, window_height = 1280, 960 
screen = p.display.set_mode(window_size) 
# board_size must be divisible by 4 or it breaks player and goblin positions.  Should be fixed once tile positions are read from external file 
board_size = board_width, board_height = 20, 20 
game_board = [[0] * board_height for i in range(board_width)] 
actor_board = [[0] * board_height for i in range(board_width)] 
mouse_pos = 0 

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
            barb_outfit=p.image.load('assets/barbarianOutfit.bmp').convert())
for i in sprites: 
    sprites[i].set_colorkey(TRANS) 
    sprites[i] = p.transform.scale(sprites[i], (TILE_DIMENSION, TILE_DIMENSION)) 

player = Player([sprites['player']], (TILE_DIMENSION*board_width//4, TILE_DIMENSION*board_height//4), TILE_DIMENSION) 
goblin = Goblin([sprites['goblin'], sprites['barb_outfit'], sprites['jester_hat']], (TILE_DIMENSION*board_width//2, TILE_DIMENSION*board_height//2), TILE_DIMENSION) 

ui = UI(window_size, board_size, 32, TILE_DIMENSION)

def create_board(board_size): 
    for y in range(board_height): 
        for x in range(board_width): 
            if x == 0 and y == 0: 
                game_board[y][x] = Tile([sprites['stoneWallCornerTL']], (x*TILE_DIMENSION, 
                y*TILE_DIMENSION), TILE_DIMENSION, 'A wall') 
            elif x == board_width-1 and y == 0: 
                game_board[y][x] = Tile([sprites['stoneWallCornerTR']], (x*TILE_DIMENSION, 
                y*TILE_DIMENSION), TILE_DIMENSION, 'A wall') 
            elif x == 0 and y == board_height-1: 
                game_board[y][x] = Tile([sprites['stoneWallCornerBL']], (x*TILE_DIMENSION, 
                y*TILE_DIMENSION), TILE_DIMENSION, 'A wall') 
            elif x == board_width-1 and y == board_height-1: 
                game_board[y][x] = Tile([sprites['stoneWallCornerBR']], (x*TILE_DIMENSION, 
                y*TILE_DIMENSION), TILE_DIMENSION, 'A wall') 
            elif y == 0 or y == board_height-1: 
                game_board[y][x] = Tile([sprites['stoneWallHori']], (x*TILE_DIMENSION, 
                y*TILE_DIMENSION), TILE_DIMENSION, 'A wall') 
            elif x == 0 or x == board_width-1: 
                game_board[y][x] = Tile([sprites['stoneWallVert']], (x*TILE_DIMENSION, 
                y*TILE_DIMENSION), TILE_DIMENSION, 'A wall')
            elif x == 0 or x == board_width-1 or y == 0 or y == board_height-1: 
                game_board[y][x] = Tile([sprites['stoneWall']], (x*TILE_DIMENSION, 
                y*TILE_DIMENSION), TILE_DIMENSION, 'A wall') 
            else: 
                game_board[y][x] = Tile([sprites['stoneFloor']], (x*TILE_DIMENSION, y*TILE_DIMENSION), TILE_DIMENSION, 'The floor') 
    actor_board[board_width//4][board_height//4] = player 
    actor_board[board_width//2][board_height//2] = goblin 

def draw_board(board_size): 
    for y in range(board_size[1]): 
        for x in range(board_size[0]): 
            can_draw(game_board[y][x]) 
            can_draw(actor_board[y][x]) 

def can_draw(tile): 
    if type(tile) != int: 
        tile.render(screen) 
    
def input(): 
    up = down = left = right = False 
    p.event.pump() 
    keys = p.key.get_pressed() 
    for e in p.event.get(): 
        if e.type == p.QUIT: 
            sys.exit() 
        if e.type == p.KEYDOWN: 
            if e.key == p.K_ESCAPE: 
                sys.exit() 

def update(): 
    global mouse_pos 
    create_board(board_size) 
    mouse_pos = p.mouse.get_pos() 

def render(): 
    global mouse_pos 
    screen.fill(BLACK) 
    draw_board(board_size) 
    ui.render(screen, GREEN, mouse_pos, game_board, actor_board) 
    p.display.flip() 
    
clock = p.time.Clock() 
done = False 
while not done: 
    input() 
    update() 
    render() 
    clock.tick(60) 

p.quit() 