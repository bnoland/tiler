import pygame as pg

class Tile(pg.sprite.Sprite):
    def __init__(self, bounds):
        super().__init__()
        self.rect = pg.Rect(bounds)
        self.image = pg.Surface(self.rect.size)
        self.image.fill((255, 255, 255))
