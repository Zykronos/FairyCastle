import pygame as p 

# Splits a sprite sheet into different sprites 
# Need to modify this to handle roguelike spritesheets 
# by adding a margin variable to account for the space 
# between individual sprites 
# Need to check whether start goes off pixels or index 
# If pixels, need to modify it to work off index 

class Sprite(object):
    """ Loads a tile sheet and returns a specified number of sprites """
    def __init__(self, sheet, start, size, col, rows=1): 
        self.frames = [] 
        for j in range(rows): 
            for i in range(col): 
                location = (start[0]+size[0]*i, start[1]+size[1]*j) 
                self.frames.append(sheet.subsurface(p.Rect(location, size))) 
        
    def sprite(self, i): 
        return self.frames[i] 