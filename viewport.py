import pygame as pg

class Viewport:
    def __init__(self, screen, map, start_pos=(0, 0)):
        self.screen = screen
        width = screen.get_width()
        height = screen.get_height()
        self.rect = pg.Rect(start_pos, (width, height))
        self.map = map

    def center_on(self, sprite):
        self.rect.center = sprite.rect.center

    def apply(self, sprite):
        return sprite.rect.move((-self.rect.x, -self.rect.y))

    def update(self, sprite):
        old_x, old_y = self.rect.topleft

        new_center = [0, 0]
        new_center[0] = sprite.rect.center[0] + \
            (self.rect.center[0] - sprite.rect.center[0]) / 1.1
        new_center[1] = sprite.rect.center[1] + \
            (self.rect.center[1] - sprite.rect.center[1]) / 1.1

        self.rect.center = new_center

        map_rect = self.map.get_rect()
        if self.rect.right > map_rect.right:
            self.rect.right = map_rect.right
        if self.rect.left < map_rect.left:
            self.rect.left = map_rect.left
        if self.rect.top < map_rect.top:
            self.rect.top = map_rect.top
        if self.rect.bottom > map_rect.bottom:
            self.rect.bottom = map_rect.bottom

        new_x, new_y = self.rect.topleft

        background_layers = self.map.get_background_layers()
        for layer in background_layers:
            x_factor, y_factor = layer.get_parallax_factors()
            for sprite in layer.get_sprites():
                sprite.rect.move_ip(
                    x_factor * (new_x - old_x), y_factor * (new_y - old_y))

    def draw(self, sprites):
        for sprite in sprites:
            self.screen.blit(sprite.image, self.apply(sprite))
