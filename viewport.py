import pygame as pg

class Viewport:
    def __init__(self, screen, map):
        self.screen = screen
        width = screen.get_width()
        height = screen.get_height()
        self.rect = pg.Rect(0, 0, width, height)
        self.map = map

    def apply(self, sprite):
        return sprite.rect.move((-self.rect.x, -self.rect.y))

    def update(self, sprite):
        self.rect.center = sprite.rect.center

        map_rect = self.map.get_rect()
        if self.rect.right > map_rect.right:
            self.rect.right = map_rect.right
        if self.rect.left < map_rect.left:
            self.rect.left = map_rect.left
        if self.rect.top < map_rect.top:
            self.rect.top = map_rect.top
        if self.rect.bottom > map_rect.bottom:
            self.rect.bottom = map_rect.bottom

    def draw(self, sprites):
        for sprite in sprites:
            self.screen.blit(sprite.image, self.apply(sprite))
