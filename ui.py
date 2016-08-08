import pygame as p 
p.init() 

''' TODO ''' 
# Display more information on the tile that the mouse is on, such as entity stats, class, equipment, 

class UI(): 
    ''' Holds all information relating to the ui '''
    def __init__(self, window_size, board_size, font_size, tile_size, SCREEN_OFFSET, cursor): 
        self.edge = (window_size[0] // 4*3, 0), (window_size[0] // 4*3, window_size[1]) 
        self.board_size = board_size[0]*tile_size, board_size[1]*tile_size 
        self.ui_pos = window_size[0] // 4*3 + 10 
        self.font_size = font_size 
        self.font = p.font.SysFont('comicsans', font_size) 
        self.tile_size = tile_size 
        self.cursor = cursor 
        self.SCREEN_OFFSET = SCREEN_OFFSET 
        self.mouse_pos = 0 
        self.mouse_index = [0, 0] 

    def update(self): 
        self.mouse_pos = (p.mouse.get_pos()[0]-self.SCREEN_OFFSET[0], p.mouse.get_pos()[1]-self.SCREEN_OFFSET[1]) 

    def render(self, screen, color, game_board, actor_board): 
        p.draw.line(screen, color, self.edge[0], self.edge[1], 2) 
        # Displays the mouse position in pixel coordinates 
        screen.blit(self.font.render(str((self.mouse_pos[0]+self.SCREEN_OFFSET[0], self.mouse_pos[1]+self.SCREEN_OFFSET[1])), 1, color), (self.ui_pos, 10)) 
        self.mouse_index = self.mouse_pos[0]//self.tile_size, self.mouse_pos[1]//self.tile_size 
        self.mouse_pos = self.mouse_pos[0], self.mouse_pos[1] 
        
        # Check to see if mouse is within bounds of the game board 
        if self.mouse_pos[0] > 0 and self.mouse_pos[0] < self.board_size[0] and self.mouse_pos[1] > 0 and self.mouse_pos[1] < self.board_size[1]: 
            # If it is, check to see what type of tile the mouse is over 
            if type(actor_board[self.mouse_index[0]][self.mouse_index[1]]) != int: 
                # If the tile is an actor, display the tile information in the ui 
                screen.blit(self.font.render(str(game_board[self.mouse_index[0]][self.mouse_index[1]]), 1, color), (self.ui_pos, 40)) 
                screen.blit(self.font.render(str(actor_board[self.mouse_index[0]][self.mouse_index[1]]), 1, color), (self.ui_pos, 80))  
            else: 
                # If the tile isn't an actor, just display the floor information 
                screen.blit(self.font.render(str(game_board[self.mouse_index[0]][self.mouse_index[1]]), 1, color), (self.ui_pos, 40)) 
            # Displays the cursor sprite on the tile the mouse is over 
            screen.blit(self.cursor, (game_board[self.mouse_index[0]][self.mouse_index[1]].pos_coordinates)) 
            # Display the position in the game board of the tile the mouse is over 
            screen.blit(self.font.render(str(game_board[self.mouse_index[0]][self.mouse_index[1]].pos_index), 1, color), (self.ui_pos+120, 10)) 
        else: 
            # If the mouse is not in the bounds of the game board 
            screen.blit(self.font.render('The ui', 1, color), (self.ui_pos, 40)) 