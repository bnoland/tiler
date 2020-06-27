import pygame as pg
import math

class Tile(pg.sprite.Sprite):
    # ``type'' is one of 'block', 'left_ramp', 'right_ramp'.
    def __init__(self, map, pos, size, friction, type='block',
                 color=(255, 255, 255),
                 collision_points=['left', 'right', 'top', 'bottom']):
        super().__init__()

        # TODO: Ensure that tile width and height are equal.
        self.rect = pg.Rect(pos, (size, size))
        self.image = pg.Surface(self.rect.size)
        self.size = size

        self.type = type
        self.collision_points = collision_points

        self.map = map
        # TODO: Should gravity be stored here?
        self.gravity = self.map.get_gravity()

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

        # pg.draw.rect(self.image, (0, 0, 255), self.image.get_rect(), 1)

        self.friction = friction

    def get_friction(self):
        return self.friction

    def get_type(self):
        return self.type

    def get_collison_points(self):
        return self.collision_points

    def get_size(self):
        return self.size

    # TODO: Later extend these methods to general entities rather than just the
    # player.

    def handle_collision(self, sprite, x_move, y_move):
        if self.type == 'block':
            self._handle_block_collision(sprite, x_move, y_move)
        elif self.type == 'left_ramp':
            self._handle_left_ramp_collision(sprite, x_move, y_move)
        elif self.type == 'right_ramp':
            self._handle_right_ramp_collision(sprite, x_move, y_move)
        else:
            # Invalid tile type.
            pass

    def _handle_block_collision(self, sprite, x_move, y_move):
        if 'left' in self.collision_points and x_move > 0:
            sprite.rect.right = self.rect.left
            sprite.vx = 0
        elif 'right' in self.collision_points and x_move < 0:
            sprite.rect.left = self.rect.right
            sprite.vx = 0
        if 'top' in self.collision_points and y_move > 0:
            sprite.rect.bottom = self.rect.top
            sprite.vy = 0
            sprite.standing_tile = self
            sprite.jump_count = 0
        elif 'bottom' in self.collision_points and y_move < 0:
            sprite.rect.top = self.rect.bottom
            sprite.vy = 0

    def _handle_left_ramp_collision(self, sprite, x_move, y_move):
        if 'bottom' in self.collision_points and y_move < 0:
            sprite.rect.top = self.rect.bottom
            sprite.vy = 0
        elif 'top' in self.collision_points and y_move > 0:
            if sprite.rect.bottom >= self.rect.bottom + \
                (sprite.rect.left - self.rect.right) and \
                sprite.rect.left >= self.rect.left:
                sprite.rect.bottom = self.rect.bottom + \
                    (sprite.rect.left - self.rect.right)
                sprite.vy = 0
                sprite.standing_tile = self
                sprite.jump_count = 0
        if 'left' in self.collision_points and x_move > 0:
            pass
        elif 'right' in self.collision_points and x_move < 0:
            if sprite.rect.bottom > self.rect.bottom and \
                sprite.rect.top < self.rect.bottom:
                sprite.rect.left = self.rect.right
                sprite.vx = 0
            elif sprite.rect.bottom >= self.rect.bottom + \
                (sprite.rect.left - self.rect.right) and \
                sprite.rect.left >= self.rect.left:
                sprite.rect.bottom = self.rect.bottom + \
                    (sprite.rect.left - self.rect.right)

    def _handle_right_ramp_collision(self, sprite, x_move, y_move):
        if 'bottom' in self.collision_points and y_move < 0:
            sprite.rect.top = self.rect.bottom
            sprite.vy = 0
        elif 'top' in self.collision_points and y_move > 0:
            if sprite.rect.bottom >= self.rect.bottom - \
                (sprite.rect.right - self.rect.left) and \
                sprite.rect.right <= self.rect.right:
                sprite.rect.bottom = self.rect.bottom - \
                    (sprite.rect.right - self.rect.left)
                sprite.vy = 0
                sprite.standing_tile = self
                sprite.jump_count = 0
        if 'left' in self.collision_points and x_move > 0:
            if sprite.rect.bottom > self.rect.bottom and \
                sprite.rect.top < self.rect.bottom:
                sprite.rect.right = self.rect.left
                sprite.vx = 0
            elif sprite.rect.bottom >= self.rect.bottom - \
                (sprite.rect.right - self.rect.left) and \
                sprite.rect.right <= self.rect.right:
                sprite.rect.bottom = self.rect.bottom - \
                    (sprite.rect.right - self.rect.left)
        elif 'right' in self.collision_points and x_move < 0:
            pass

    def handle_physics(self, sprite, dt):
        if self.type == 'block':
            self._handle_block_physics(sprite, dt)
        elif self.type == 'left_ramp':
            self._handle_left_ramp_physics(sprite, dt)
        elif self.type == 'right_ramp':
            self._handle_right_ramp_physics(sprite, dt)
        else:
            # Invalid tile type.
            pass

    def _handle_block_physics(self, sprite, dt):
        sprite.vx += self.friction * -sprite.vx * dt
        sprite.vy += self.gravity * dt

    def _handle_left_ramp_physics(self, sprite, dt):
        theta = math.pi / 180 * 45
        normal = self.gravity * math.cos(theta)
        slide = self.gravity * math.sin(theta)
        sprite.vy += normal * math.cos(theta) * dt
        sprite.vx += slide * math.sin(theta) * dt
        sprite.vy += slide * math.cos(theta) * dt
        sprite.vx += self.friction * -sprite.vx * dt
        sprite.vy += self.friction * -sprite.vy * dt

    def _handle_right_ramp_physics(self, sprite, dt):
        theta = math.pi / 180 * 45
        normal = self.gravity * math.cos(theta)
        slide = self.gravity * math.sin(theta)
        sprite.vy += normal * math.cos(theta) * dt
        sprite.vx += -slide * math.sin(theta) * dt
        sprite.vy += -slide * math.cos(theta) * dt
        sprite.vx += self.friction * -sprite.vx * dt
        sprite.vy += self.friction * -sprite.vy * dt

class EarthTile(Tile):
    def __init__(self, map, pos, size, type='block',
                 collision_points=['left', 'right', 'top', 'bottom']):
        super().__init__(
            map, pos, size, 0.7, type, collision_points=collision_points)

class IceTile(Tile):
    def __init__(self, map, pos, size, type='block',
                 collision_points=['left', 'right', 'top', 'bottom']):
        super().__init__(
            map, pos, size, 0, type, (0, 0, 255), collision_points=collision_points)
