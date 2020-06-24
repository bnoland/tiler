import pygame as pg

class Tile(pg.sprite.Sprite):
    # ``type'' is one of 'block', 'left_ramp', 'right_ramp'.
    def __init__(self, pos, size, friction, type='block',
                 color=(255, 255, 255),
                 collision_points=['left', 'right', 'top', 'bottom']):
        super().__init__()

        # TODO: Ensure that tile width and height are equal.
        self.rect = pg.Rect(pos, (size, size))
        self.image = pg.Surface(self.rect.size)
        self.size = size

        self.type = type
        self.collision_points = collision_points

        if self.type == 'block':
            self.image.fill(color)
        elif self.type == 'left_ramp':
            points = (
                (0, 0),
                (0, self.size-1),
                (self.size-1, self.size-1)
            )
            pg.draw.polygon(self.image, color, points)
            self.image.set_colorkey((0, 0, 0))
        elif self.type == 'right_ramp':
            points = (
                (0, self.size-1),
                (self.size-1, self.size-1),
                (self.size-1, 0)
            )
            pg.draw.polygon(self.image, color, points)
            self.image.set_colorkey((0, 0, 0))

        if 'left' in self.collision_points:
            pg.draw.line(self.image, (255, 0, 0),
                (0, 0), (0, self.size-1))
        if 'right' in self.collision_points:
            pg.draw.line(self.image, (255, 0, 0),
                (self.size-1, 0),
                (self.size-1, self.size-1))
        if 'top' in self.collision_points:
            pg.draw.line(self.image, (255, 0, 0),
                (0, 0), (self.size-1, 0))
        if 'bottom' in self.collision_points:
            pg.draw.line(self.image, (255, 0, 0),
                (0, self.size-1),
                (self.size-1, self.size-1))

        self.friction = friction

    def get_friction(self):
        return self.friction

    def get_type(self):
        return self.type

    def get_collison_points(self):
        return self.collision_points

    def get_size(self):
        return self.size

class EarthTile(Tile):
    def __init__(self, pos, size, type='block',
                 collision_points=['left', 'right', 'top', 'bottom']):
        super().__init__(
            pos, size, 0.7, type, collision_points=collision_points)

class IceTile(Tile):
    def __init__(self, pos, size, type='block',
                 collision_points=['left', 'right', 'top', 'bottom']):
        super().__init__(
            pos, size, 0, type, (0, 0, 255), collision_points=collision_points)
