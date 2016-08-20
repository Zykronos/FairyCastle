import pygame as p 
from tile import * 
p.init() 

''' TODO ''' 
# Add combat method once appropriate stats are added to Tile class 
# Use distance formula for enemy ai i.e. once the player's within a certain range of the enemy, the enemy starts moving toward the player 
# can_move should be here rather than in game.py.  This will allow enemies to move without a lot of extra code 

class Player(Tile): 
    def __init__(self, sprite, pos, tile_size, name='A tile', walkable=True): 
        super().__init__(sprite, pos, tile_size, name, walkable) 
        self.hp = 8 
        self.lives = 1 
        self.id = 'player' 
        self.job = 'peasant' 
        self.name = 'A {0}'.format(self.job) 
        self.alive = True if (self.hp > 0) else False 
        self.is_walkable = walkable if not self.alive else False 
        self.vision = 8 

        self.mining = 1 
        self.smithing = 1 
        self.woodcutting = 1 
        self.farming = 1 
        self.melee = 1 
        self.archery = 1 
        self.magic = 1 
        self.fletching = 1 
        self.runecrafting = 1 

    def move(self, direction): 
        if direction == 'up': 
            self.pos_index[1] -= 1  
        if direction == 'down': 
            self.pos_index[1] += 1 
        if direction == 'left': 
            self.pos_index[0] -= 1 
        if direction == 'right': 
            self.pos_index[0] += 1 
        