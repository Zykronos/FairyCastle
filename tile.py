import pygame as p 
p.init() 

''' TODO ''' 
# Add position to the class both in terms of array position and pixel position 
# Make movement purely tile based, with pixel calculations going on in the background 
# Add additional stats 
# Implement support for tiles larger than 1x1 e.g. to support a fully grown tree that's 1x2 or a dragon that's 4x4 

class Tile(): 
    def __init__(self, sprite, pos, tile_size, name='A tile', walkable=True): 
        self.pos_coordinates = pos[0], pos[1] 
        self.pos_index = pos[0]//tile_size, pos[1]//tile_size 
        self.sprite = sprite 
        self.is_walkable = walkable 
        self.name = name 
        self.id = 'tile' 

    def __str__(self): 
        return self.name 

    def render(self, screen): 
        for i in self.sprite: 
            screen.blit(i, self.pos_coordinates) 