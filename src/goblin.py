import pygame as p 
from player import * 
p.init() 

''' TODO ''' 
# Add combat method once appropriate stats are added to Tile class 

class Goblin(Player): 
    def __init__(self, sprite, pos, tile_size, name='A tile', walkable=False): 
        super().__init__(sprite, pos, tile_size, name, walkable) 
        self.hp = 4 
        self.mp = 0 
        self.name = 'A goblin' 
        self.id = 'enemy' 
