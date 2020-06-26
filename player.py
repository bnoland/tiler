import pygame as pg
import math

class Player(pg.sprite.Sprite):
    def __init__(self, map, pos, size):
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

        # Allows for double-jumping, etc.
        self.jump_count = 0
        self.max_jumps = 2

        # Tile the player is currently standing on.
        self.standing_tile = None

        self.walking_left = False
        self.walking_right = False
        self.running = False
        self.jumping = False

    def jump(self):
        self.jumping = True

    def on_surface(self):
        return self.standing_tile is not None and not self.jumping

    def start_walking_left(self):
        self.walking_left = True

    def stop_walking_left(self):
        self.walking_left = False

    def start_walking_right(self):
        self.walking_right = True

    def stop_walking_right(self):
        self.walking_right = False

    def start_running(self):
        self.running = True

    def stop_running(self):
        self.running = False

    def physics_step(self, dt):
        if self.on_surface():
            friction = self.standing_tile.get_friction()

            run_factor = 1.5 if self.running else 1.0
            if self.walking_left:
                self.vx += -15 * friction * run_factor * dt
            if self.walking_right:
                self.vx += 15 * friction * run_factor * dt

            tile_type = self.standing_tile.get_type()
            if tile_type == 'block':
                self.vx += friction * -self.vx * dt
                self.vy += self.gravity * dt
            elif tile_type == 'left_ramp':
                theta = math.pi / 180 * 45
                normal = self.gravity * math.cos(theta)
                slide = self.gravity * math.sin(theta)
                self.vy += normal * math.cos(theta) * dt
                self.vx += slide * math.sin(theta) * dt
                self.vy += slide * math.cos(theta) * dt
                self.vx += friction * -self.vx * dt
                self.vy += friction * -self.vy * dt
            elif tile_type == 'right_ramp':
                theta = math.pi / 180 * 45
                normal = self.gravity * math.cos(theta)
                slide = self.gravity * math.sin(theta)
                self.vy += normal * math.cos(theta) * dt
                self.vx += -slide * math.sin(theta) * dt
                self.vy += -slide * math.cos(theta) * dt
                self.vx += friction * -self.vx * dt
                self.vy += friction * -self.vy * dt
            else:
                # Invalid tile type.
                pass
        else:
            self.vy += self.gravity * dt

        if self.jumping and self.jump_count < self.max_jumps:
            self.jump_count += 1
            self.vy += -40 * dt

        self.jumping = False  # Completed jump, if any

        # Limit velocity components to half a tile width to ensure the player
        # doesn't clip through a collideable tile.
        max_step = self.map.get_tile_size() // 2
        if abs(self.vx) * dt > max_step:
            self.vx = math.copysign(max_step / dt, self.vx)
        if abs(self.vy) * dt > max_step:
            self.vy = math.copysign(max_step / dt, self.vy)

        dx = self.vx * dt
        dy = self.vy * dt
        self.move(dx, dy)

    def move(self, dx, dy):
        # print(dx, dy)
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
                collision_points = tile.get_collison_points()

                if tile.get_type() == 'block':
                    if 'left' in collision_points and dx > 0:
                        self.rect.right = tile.rect.left
                        self.vx = 0
                    elif 'right' in collision_points and dx < 0:
                        self.rect.left = tile.rect.right
                        self.vx = 0
                    if 'top' in collision_points and dy > 0:
                        self.rect.bottom = tile.rect.top
                        self.vy = 0
                        self.standing_tile = tile
                        self.jump_count = 0
                    elif 'bottom' in collision_points and dy < 0:
                        self.rect.top = tile.rect.bottom
                        self.vy = 0
                elif tile.get_type() == 'left_ramp':
                    # TODO: Reform!!
                    if self.rect.bottom >= tile.rect.bottom + \
                        (self.rect.left - tile.rect.right) and \
                        self.rect.left >= tile.rect.left:
                        if 'bottom' in collision_points and dy < 0:
                            self.rect.top = tile.rect.bottom
                            self.vy = 0
                        elif 'top' in collision_points and \
                            (dy > 0 or math.isclose(dx, 0)):
                            self.rect.bottom = tile.rect.bottom + \
                                (self.rect.left - tile.rect.right)
                            self.vy = 0
                            self.standing_tile = tile
                            self.jump_count = 0
                elif tile.get_type() == 'right_ramp':
                    if 'bottom' in collision_points and dy < 0:
                        self.rect.top = tile.rect.bottom
                        self.vy = 0
                    elif 'top' in collision_points and dy > 0:
                        if self.rect.bottom >= tile.rect.bottom - \
                            (self.rect.right - tile.rect.left) and \
                            self.rect.right <= tile.rect.right:

                            self.rect.bottom = tile.rect.bottom - \
                                (self.rect.right - tile.rect.left)
                            self.vy = 0
                            self.standing_tile = tile
                            self.jump_count = 0

                    # if 'left' in collision_points and dx > 0:
                    #     # TODO: Doesn't work well as-is with ramps consisting of
                    #     # multiple ramp tiles.
                    #     if self.rect.bottom > tile.rect.bottom and \
                    #         self.rect.top < tile.rect.bottom:
                    #         self.rect.right = tile.rect.left
                    #         self.vx = 0
                    #         print('top:', self.rect.top, tile.rect.bottom)
                    #         print('bottom:', self.rect.bottom, tile.rect.bottom)
                    #     elif self.rect.bottom >= tile.rect.bottom - \
                    #         (self.rect.right - tile.rect.left) and \
                    #         self.rect.right <= tile.rect.right:
                    #         self.rect.bottom = tile.rect.bottom - \
                    #             (self.rect.right - tile.rect.left)
                    # elif 'right' in collision_points and dx < 0:
                    #     pass
                else:
                    # Invalid tile type.
                    pass

        self.x = self.rect.x
        self.y = self.rect.y
