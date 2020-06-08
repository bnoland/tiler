import pygame as pg
from tile import Tile

class Map:
    def __init__(self, string_rep, tile_size):
        super().__init__()
        self.tile_group = pg.sprite.Group()
        self.tile_width, self.tile_height = tile_size
        self._build_from_string(string_rep)

    def _build_from_string(self, string_rep):
        for i, row in enumerate(string_rep):
            for j, col in enumerate(row):
                if col == 'x':
                    bounds = (
                        self.tile_width * j, self.tile_height * i,
                        self.tile_width, self.tile_height
                    )
                    new_tile = Tile(bounds)
                    self.tile_group.add(new_tile)

    def draw(self, screen):
        self.tile_group.draw(screen)

    def get_tile_group(self):
        return self.tile_group
