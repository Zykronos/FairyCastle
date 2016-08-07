import pygame as p 
p.init() 

''' TODO ''' 
# Display more information on the tile that the mouse is on, such as entity stats, class, equipment, 

class UI(): 
    def __init__(self, window_size, board_size, font_size, tile_size): 
        self.edge = (window_size[0] // 4*3, 0), (window_size[0] // 4*3, window_size[1]) 
        self.board_size = board_size[0]*tile_size, board_size[1]*tile_size 
        self.ui_pos = window_size[0] // 4*3 + 10 
        self.font_size = font_size 
        self.font = p.font.SysFont('comicsans', font_size) 
        self.tile_size = tile_size 

    def render(self, screen, color, mouse_pos, game_board, actor_board): 
        mouse_index = mouse_pos[0]//self.tile_size, mouse_pos[1]//self.tile_size 
        p.draw.line(screen, color, self.edge[0], self.edge[1], 2) 
        screen.blit(self.font.render(str(mouse_pos), 1, color), (self.ui_pos, 10)) 
         
        if mouse_pos[0] < self.board_size[0] and mouse_pos[1] < self.board_size[1]: 
            if type(actor_board[mouse_index[0]][mouse_index[1]]) != int: 
                screen.blit(self.font.render(str(game_board[mouse_index[0]][mouse_index[1]]), 1, color), (self.ui_pos, 40)) 
                screen.blit(self.font.render(str(actor_board[mouse_index[0]][mouse_index[1]]), 1, color), (self.ui_pos, 80))  
            else: # An elif should be added here when items (such as barrels and crates) are added to game_board 
                screen.blit(self.font.render(str(game_board[mouse_index[0]][mouse_index[1]]), 1, color), (self.ui_pos, 40)) 
            screen.blit(self.font.render(str(game_board[mouse_index[0]][mouse_index[1]].pos_index), 1, color), (self.ui_pos+120, 10))  
        else: 
            screen.blit(self.font.render('The ui', 1, color), (self.ui_pos, 40)) 