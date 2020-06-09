import pygame as pg
from tile import Tile
from player import Player

class Map:
    def __init__(self, string_rep, tile_size, player_size):
        super().__init__()
        self.tile_list = []
        self.tile_width, self.tile_height = tile_size

        self.player_size = player_size

        # TODO: Rather crude width/height calculations based on string
        # representation.
        self.width = len(string_rep[0]) * self.tile_width
        self.height = len(string_rep) * self.tile_height
        self.rect = pg.Rect(0, 0, self.width, self.height)

        self._build_from_string(string_rep)

    def get_rect(self):
        return self.rect

    def get_player(self):
        return self.player

    def _build_from_string(self, string_rep):
        for i, row in enumerate(string_rep):
            for j, col in enumerate(row):
                x, y = self.tile_width * j, self.tile_height * i
                if col == 'x':
                    bounds = (
                        x, y,
                        self.tile_width, self.tile_height
                    )
                    new_tile = Tile(bounds)
                    self.tile_list.append(new_tile)
                elif col == 'p':
                    self.player = Player(self, self.player_size, (x, y))

    def get_tiles(self):
        return self.tile_list
