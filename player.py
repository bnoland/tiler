import pygame as pg

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

        self.x = self.rect.x
        self.y = self.rect.y
        self.vx = 0
        self.vy = 0
        self.ax = 0  # TODO: No longer use this
        self.ay = 1.5  # TODO: Set world gravity

        # Allows for double-jumping, etc.
        self.jump_count = 0
        self.max_jumps = 2

        # self.on_surface = False
        self.standing_tile = None  # Tile currently standing on.

    def jump(self):
        if self.on_surface():
            self.jump_count = 0

        if self.jump_count < self.max_jumps:
            self.jump_count += 1
            self.vy = -20

    def on_surface(self):
        return self.standing_tile is not None

    def handle_horizontal_movement(self, pressed_keys, mods):
        if pressed_keys[pg.K_LEFT] or pressed_keys[pg.K_RIGHT]:
            if self.on_surface():
                if pressed_keys[pg.K_LEFT]:
                    # self.ax = -0.75
                    self.vx = -6
                elif pressed_keys[pg.K_RIGHT]:
                    # self.ax = 0.75
                    self.vx = 6
                if mods & pg.KMOD_SHIFT:
                    # Run when shift pressed.
                    # self.ax *= 1.5
                    self.vx *= 1.5
            else:
                # No horizontal acceleration when mid-air.
                self.ax = 0
        else:
            self.ax = 0

    def physics_step(self, dt):
        print(self.vx, self.vy)

        # TODO: Need overhaul of friction system to account for ramps.
        if self.on_surface():
            # Add friction when on a surface.
            friction = self.standing_tile.get_friction()
            self.vx += dt * -self.vx * friction

        self.vx += dt * self.ax
        self.vy += dt * self.ay

        dx = dt * self.vx
        dy = dt * self.vy

        self.move(dx, dy)

    def move(self, dx, dy):
        self.move_single_axis(dx, 0)
        self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        self.x += dx
        self.y += dy

        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

        # self.on_surface = False
        self.standing_tile = None

        for tile in self.map.get_tiles():
            if self.rect.colliderect(tile.rect):
                if tile.get_type() == 'block':
                    # The player can get stuck on multi-tile ramps if we set the
                    # horizontal velocity to zero on horizontal collisions, so
                    # we don't do this here.
                    # TODO: Better work-around?
                    if dx > 0:
                        self.rect.right = tile.rect.left
                        # self.vx = 0
                    elif dx < 0:
                        self.rect.left = tile.rect.right
                        # self.vx = 0
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
