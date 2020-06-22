import pygame as pg
import math

def sgn(x):
    if math.isclose(x, 0):
        return 0
    elif x < 0:
        return -1
    elif x > 0:
        return 1

# TODO: Overhaul/cleanup of physics system needed.
class Player(pg.sprite.Sprite):
    def __init__(self, map, size, pos):
        super().__init__()

        self.map = map

        self.width, self.height = size
        self.image = pg.Surface((self.width, self.height))
        self.image.fill((0, 0, 255))
        pg.draw.rect(self.image, (255, 0, 0), self.image.get_rect(), 1)
        self.rect = self.image.get_rect(topleft=pos)

        self.gravity = self.map.get_gravity()

        self.x = self.rect.x
        self.y = self.rect.y
        self.vx = 0
        self.vy = 0
        # self.ax = 0
        # self.ay = self.gravity

        # Allows for double-jumping, etc.
        self.jump_count = 0
        self.max_jumps = 2

        self.standing_tile = None  # Tile currently standing on

    def jump(self):
        if self.on_surface():
            self.jump_count = 0

        if self.jump_count < self.max_jumps:
            self.jump_count += 1
            self.vy = -20

    def on_surface(self):
        return self.standing_tile is not None

    def is_moving(self):
        return abs(self.vx) > 0 or abs(self.vy) > 0
        # return self.speed() > 0

    def speed(self):
        return math.sqrt(self.vx**2 + self.vy**2)

    def handle_horizontal_movement(self, pressed_keys, mods):
        if pressed_keys[pg.K_LEFT] or pressed_keys[pg.K_RIGHT]:
            if self.on_surface():
                if pressed_keys[pg.K_LEFT]:
                    self.vx = -6
                elif pressed_keys[pg.K_RIGHT]:
                    self.vx = 6
                if mods & pg.KMOD_SHIFT:
                    # Run when shift pressed.
                    self.vx *= 1.5

    def physics_step(self, dt):
        # print(self.vx, self.vy)

        if self.on_surface():
            tile_type = self.standing_tile.get_type()
            friction = self.standing_tile.get_friction()

            if tile_type == 'block':
                self.vx += friction * -self.vx * dt
                self.vy += self.gravity * dt
            elif tile_type == 'left_ramp':
                pass
            elif tile_type == 'right_ramp':
                theta = math.pi / 180 * 45
                N = -self.gravity * math.cos(theta)
                self.vx += N * math.sin(theta) * dt
                self.vy += self.gravity + N * math.cos(theta) * dt
                # speed = self.speed()
                # sign = sgn(self.vx)
                # self.vx += -sign * friction * speed * math.cos(theta) * dt
                # self.vy += sign * friction * speed * math.sin(theta) * dt
            else:
                # Invalid tile type.
                pass
        else:
            self.vy += self.gravity * dt

        dx = self.vx * dt
        dy = self.vy * dt
        self.move(dx, dy)

    def move(self, dx, dy):
        self.move_single_axis(dx, 0)
        self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        self.x += dx
        self.y += dy

        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

        self.standing_tile = None

        for tile in self.map.get_tiles():
            if self.rect.colliderect(tile.rect):
                if tile.get_type() == 'block':
                    if dx > 0:
                        self.rect.right = tile.rect.left
                        self.vx = 0
                    elif dx < 0:
                        self.rect.left = tile.rect.right
                        self.vx = 0
                    if dy > 0:
                        self.rect.bottom = tile.rect.top
                        self.vy = 0
                        self.standing_tile = tile
                    elif dy < 0:
                        self.rect.top = tile.rect.bottom
                        self.vy = 0
                elif tile.get_type() == 'left_ramp':
                    # TODO: Implement.
                    pass
                elif tile.get_type() == 'right_ramp':
                    if self.rect.bottom >= tile.rect.bottom - \
                        (self.rect.right - tile.rect.left) and \
                        self.rect.right <= tile.rect.right:
                        if dy < 0:
                            self.rect.top = tile.rect.bottom
                            self.vy = 0
                        elif dy > 0:
                            self.rect.bottom = tile.rect.bottom - \
                                (self.rect.right - tile.rect.left)
                            self.vy = 0
                            self.standing_tile = tile
                else:
                    # Invalid tile type.
                    pass

        self.x = self.rect.x
        self.y = self.rect.y
