class Floor(Tile): 
    def __init__(self, sprite, pos_index, TILE_SIZE): 
        super().__init__(sprite, pos, tile_size, name, walkable) 
        self.sprite = sprite 
        self.pos = pos_index 
        self.name = "The floor"
        self.walkable = True 