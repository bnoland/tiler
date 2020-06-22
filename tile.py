import pygame as pg

class Tile(pg.sprite.Sprite):
    # ``type'' is one of 'block', 'left_ramp', 'right_ramp'.
    def __init__(self, bounds, friction=0.1, type='block',
                 color=(255, 255, 255)):
        super().__init__()
        self.rect = pg.Rect(bounds)
        self.image = pg.Surface(self.rect.size)

        self.type = type

        if self.type == 'block':
            self.image.fill(color)
        elif self.type == 'left_ramp':
            points = (
                (0, 0),
                (0, self.rect.height-1),
                (self.rect.width-1, self.rect.height-1)
            )
            pg.draw.polygon(self.image, color, points)
            self.image.set_colorkey((0, 0, 0))
        elif self.type == 'right_ramp':
            points = (
                (0, self.rect.height-1),
                (self.rect.width-1, self.rect.height-1),
                (self.rect.width-1, 0)
            )
            pg.draw.polygon(self.image, color, points)
            self.image.set_colorkey((0, 0, 0))

        pg.draw.rect(self.image, (255, 0, 0), self.image.get_rect(), 1)

        self.friction = friction

    def get_friction(self):
        return self.friction

    def get_type(self):
        return self.type

class EarthTile(Tile):
    def __init__(self, bounds, type='block'):
        super().__init__(bounds, 0.9, type)

class IceTile(Tile):
    def __init__(self, bounds, type='block'):
        super().__init__(bounds, 0, type, (0, 0, 255))
