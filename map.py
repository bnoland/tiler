import pygame as pg
from tile import Tile, EarthTile, IceTile
from player import Player

class Map:
    def __init__(self, string_rep, tile_size, player_size, gravity,
                 background_layers=[]):
        super().__init__()
        self.tile_list = []
        self.tile_size = tile_size

        self.player_size = player_size
        self.gravity = gravity

        self.background_layers = background_layers

        # TODO: Rather crude width/height calculations based on string
        # representation.
        self.width = len(string_rep[0]) * self.tile_size
        self.height = len(string_rep) * self.tile_size
        self.rect = pg.Rect(0, 0, self.width, self.height)

        self._build_from_string(string_rep)

    def get_rect(self):
        return self.rect

    def get_player(self):
        return self.player

    def get_gravity(self):
        return self.gravity

    def get_tile_size(self):
        return self.tile_size

    def get_background_layers(self):
        return self.background_layers

    def _build_from_string(self, string_rep):
        is_not_tile = lambda c: c == 'p' or c == ' '

        for i, row in enumerate(string_rep):
            for j, col in enumerate(row):
                x, y = self.tile_size * j, self.tile_size * i
                if col == 'p':
                    self.player = Player(self, (x, y), self.player_size)
                elif col != ' ':
                    # Quick n' dirty automated collision point generation.
                    collision_points = []
                    if i > 0:
                        if is_not_tile(string_rep[i-1][j]):
                            collision_points.append('top')
                    if i < len(string_rep)-1:
                        if is_not_tile(string_rep[i+1][j]):
                            collision_points.append('bottom')
                    if j > 0:
                        if is_not_tile(string_rep[i][j-1]):
                            collision_points.append('left')
                    if j < len(row)-1:
                        if is_not_tile(string_rep[i][j+1]):
                            collision_points.append('right')

                    # Earth tiles
                    if col == '0':
                        new_tile = EarthTile(self, (x, y), self.tile_size,
                            type='block', collision_points=collision_points)
                    elif col == '1':
                        new_tile = EarthTile(self, (x, y), self.tile_size,
                            type='left_ramp',
                            collision_points=collision_points)
                    elif col == '2':
                        new_tile = EarthTile(self, (x, y), self.tile_size,
                            type='right_ramp',
                            collision_points=collision_points)
                    # Ice tiles
                    elif col == '3':
                        new_tile = IceTile(self, (x, y), self.tile_size,
                            type='block', collision_points=collision_points)
                    elif col == '4':
                        new_tile = IceTile(self, (x, y), self.tile_size,
                            type='left_ramp',
                            collision_points=collision_points)
                    elif col == '5':
                        new_tile = IceTile(self, (x, y), self.tile_size,
                            type='right_ramp',
                            collision_points=collision_points)
                    else:
                        # Invalid tile.
                        pass

                    self.tile_list.append(new_tile)
                else:
                    # Invalid specification.
                    pass

    def get_tiles(self):
        return self.tile_list
