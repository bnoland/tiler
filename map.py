import pygame as pg
from tile import Tile, EarthTile, IceTile
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
        friction = 0.1  # Tile friction

        for i, row in enumerate(string_rep):
            for j, col in enumerate(row):
                x, y = self.tile_width * j, self.tile_height * i
                if col == 'p':
                    self.player = Player(self, self.player_size, (x, y))
                elif col != ' ':
                    # It's a tile.
                    bounds = (
                        x, y,
                        self.tile_width, self.tile_height
                    )
                    # Earth tiles
                    if col == '0':
                        new_tile = EarthTile(bounds=bounds, type='block')
                    elif col == '1':
                        new_tile = EarthTile(bounds=bounds, type='left_ramp')
                    elif col == '2':
                        new_tile = EarthTile(bounds=bounds, type='right_ramp')
                    # Ice tiles
                    elif col == '3':
                        new_tile = IceTile(bounds=bounds, type='block')
                    elif col == '4':
                        new_tile = IceTile(bounds=bounds, type='left_ramp')
                    elif col == '5':
                        new_tile = IceTile(bounds=bounds, type='right_ramp')
                    else:
                        # Invalid tile.
                        pass
                    self.tile_list.append(new_tile)
                else:
                    # Invalid specification.
                    pass

    def get_tiles(self):
        return self.tile_list
