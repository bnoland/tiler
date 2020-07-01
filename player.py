import pygame as pg
import math

class Player(pg.sprite.Sprite):
    def __init__(self, map, pos, size):
        super().__init__()

        self.width, self.height = size
        self.image = pg.Surface((self.width, self.height))
        self.image.fill((0, 0, 255))
        pg.draw.rect(self.image, (255, 0, 0), self.image.get_rect(), 1)
        self.rect = self.image.get_rect(topleft=pos)

        self.map = map
        # TODO: Should gravity be stored here?
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
            # TODO: Move to tile physics handler?
            friction = self.standing_tile.get_friction()
            run_factor = 1.5 if self.running else 1.0
            if self.walking_left:
                self.vx += -22 * friction * run_factor * dt
            if self.walking_right:
                self.vx += 22 * friction * run_factor * dt

            self.standing_tile.handle_physics(self, dt)
        else:
            self.vy += self.gravity * dt

        if self.jumping and self.jump_count < self.max_jumps:
            self.jump_count += 1
            # TODO: self.vy = -20 * dt instead??
            self.vy += -20 * dt

        self.jumping = False  # Completed jump, if any

        dx = round(self.vx * dt)
        dy = round(self.vy * dt)
        self._move(dx, dy)

    # def _move(self, dx, dy):
    #     x_move, y_move = math.copysign(1, dx), math.copysign(1, dy)
    #     x_steps, y_steps = abs(dx), abs(dy)
    #     for _ in range(x_steps):
    #         self._step_single_axis(x_move, 0)
    #     for _ in range(y_steps):
    #         self._step_single_axis(0, y_move)

    def _move(self, dx, dy):
        # TODO: Stop moving pixel-wise when no longer any velocity in that
        # direction?
        if dx == 0:
            # Player is moving vertically.
            y_steps = abs(dy)
            y_move = math.copysign(1, dy)
            for _ in range(y_steps):
                self._step_single_axis(0, y_move)
        else:
            # Player is moving at some non-zero angle with the vertical.
            rate = dy / dx
            x_steps = abs(dx)
            y_accum = 0
            x_move = math.copysign(1, dx)
            y_move = math.copysign(1, dy)
            for _ in range(x_steps):
                self._step_single_axis(x_move, 0)
                y_accum += abs(rate)
                y_steps = int(y_accum)
                y_accum -= y_steps
                for _ in range(y_steps):
                    self._step_single_axis(0, y_move)

            # Perform any remaining vertical steps.
            y_steps = round(y_accum)
            for _ in range(y_steps):
                self._step_single_axis(0, y_move)

    def _step_single_axis(self, x_move, y_move):
        self.rect.move_ip(x_move, y_move)

        self.standing_tile = None

        for tile in self.map.get_tiles():
            if self.rect.colliderect(tile.rect):
                tile.handle_collision(self, x_move, y_move)

        self.x = self.rect.x
        self.y = self.rect.y
