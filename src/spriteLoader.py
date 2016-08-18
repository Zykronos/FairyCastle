import pygame as p 

# Splits a sprite sheet into different sprites 
# Need to modify this to handle roguelike spritesheets 
# by adding a margin variable to account for the space 
# between individual sprites 
# Need to check whether start goes off pixels or index 
# If pixels, need to modify it to work off index 

class Sprite(object):
    ''' Loads a tile sheet and returns a specified number of sprites ''' 
    def __init__(self, sheet, start, size, margin, col, rows=1): 
        self.frames = [] 
        self.col = col 
        self.rows = rows 
        self.start = (start[0]+margin, start[1]+margin)
        for j in range(rows): 
            for i in range(col): 
                location = (self.start[0]+size*i+margin*i, self.start[1]+size*j+margin*j) 
                self.frames.append(sheet.subsurface(p.Rect(location, (size, size)))) 
        
    def sprite(self, x, y): 
        return self.frames[self.col*y+x] 
