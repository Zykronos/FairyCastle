import pygame as p 
from tile import * 
p.init() 

''' TODO ''' 
# Add combat method once appropriate stats are added to Tile class 

class Player(Tile): 
    def __init__(self, sprite, pos, tile_size, name='A tile', walkable=True): 
        super().__init__(sprite, pos, tile_size, name, walkable) 
        self.hp = 8 
        self.mp = 0 
        self.id = 'player' 
        self.job = 'peasant' 
        self.name = 'A {0}'.format(self.job) 
        self.alive = True if (self.hp > 0) else False 
        self.is_walkable = walkable if not self.alive else False 

        self.mining = 1 
        self.smithing = 1 
        self.woodcutting = 1 
        self.farming = 1 
        self.melee = 1 
        self.archery = 1 
        self.fletching = 1 

    def move(self, direction): 
        if direction == 'up': 
            self.pos_index[1] -= 1  
        if direction == 'down': 
            self.pos_index[1] += 1 
        if direction == 'left': 
            self.pos_index[0] -= 1 
        if direction == 'right': 
            self.pos_index[0] += 1 
        #self.pos_coordinates = self.pos_index[0]*self.tile_size+self.SCREEN_OFFSET[0], self.pos_index[1]*self.tile_size+self.SCREEN_OFFSET[1] 
