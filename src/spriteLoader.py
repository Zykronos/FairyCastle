import pygame as p 

class Sprite(object):
    ''' Loads a tile sheet and returns a specified number of sprites ''' 
    def __init__(self, sheet, TILE_DIMENSION, start, size, margin, col, rows=1): 
        self.sprites = [[0]*rows for x in range(col)] 
        self.start = (start[0]+margin, start[1]+margin)
        for j in range(rows): 
            for i in range(col): 
                location = (self.start[0]+size*i+margin*i, self.start[1]+size*j+margin*j) 
                self.sprites[i][j] = sheet.subsurface(p.Rect(location, (size, size))) 
                self.sprites[i][j] = p.transform.scale(self.sprites[i][j], (TILE_DIMENSION, TILE_DIMENSION)) 
        
    def sprite(self, x, y): 
        return self.frames[self.col*y+x] 
