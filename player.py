import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self, map, size, pos):
        super().__init__()

        self.map = map

        self.width, self.height = size
        self.image = pg.Surface((self.width, self.height))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=pos)

        self.x = self.rect.x
        self.y = self.rect.y
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 5  # TODO: Set world gravity

        # Allows for double-jumping, etc.
        self.jump_count = 0
        self.max_jumps = 2

        self.on_surface = False

    def jump(self):
        if self.on_surface:
            self.jump_count = 0

        if self.jump_count < self.max_jumps:
            self.jump_count += 1
            self.vy = -40

    def handle_horizontal_movement(self, pressed_keys, mods):
        if pressed_keys[pg.K_LEFT] or pressed_keys[pg.K_RIGHT]:
            if self.on_surface:
                if pressed_keys[pg.K_LEFT]:
                    self.ax = -1.5
                elif pressed_keys[pg.K_RIGHT]:
                    self.ax = 1.5
                if mods & pg.KMOD_SHIFT:
                    # Run when shift pressed.
                    self.ax *= 2
            else:
                # No horizontal acceleration when mid-air.
                self.ax = 0
        else:
            self.ax = 0

    def physics_step(self, dt):
        if self.on_surface:
            # Add friction when on a surface.
            friction_factor = 0.1
            self.vx += dt * -self.vx * friction_factor

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

        self.on_surface = False

        for tile in self.map.get_tiles():
            if self.rect.colliderect(tile.rect):
                if dx > 0:    # Moving right, hit left of tile
                    self.rect.right = tile.rect.left
                    self.vx = 0
                elif dx < 0:  # Moving left, hit right of tile
                    self.rect.left = tile.rect.right
                    self.vx = 0
                if dy > 0:    # Moving down, hit top of tile
                    self.rect.bottom = tile.rect.top
                    self.vy = 0
                    self.on_surface = True
                elif dy < 0:  # Moving up, hit bottom of tile
                    self.rect.top = tile.rect.bottom
                    self.vy = 0

                self.x = self.rect.x
                self.y = self.rect.y
