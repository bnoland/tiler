import pygame as pg
import math

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)

def rotate(v, theta):
    wx = math.cos(theta) * v[0] - math.sin(theta) * v[1]
    wy = math.sin(theta) * v[0] + math.cos(theta) * v[1]
    return [wx, wy]

def normalize(v):
    norm = math.sqrt(v[0] * v[0] + v[1] * v[1])
    return [v[0] / norm, v[1] / norm]

class Map:
    def __init__(self):
        # TODO: Just a fixed map for now.
        self.squares = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,2,2,2,2,0,0,0,0,2,0,2,0,2,0,0,0,1],
            [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,2,0,0,0,2,0,0,0,1],
            [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,2,0,2,2,0,0,0,0,2,0,2,0,2,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,0,0,0,0,2,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]

        self.width = len(self.squares[0])
        self.height = len(self.squares)

        # TODO: In general might want to do texture loading *outside* of the map
        # class.
        self.textures = [
            pg.image.load('marble_color.png').convert(),
            pg.image.load('cloud_color.png').convert()
        ]

        self.texture_size = 64  # Fixed for now.

        self.texture_pixels = [
            pg.PixelArray(texture)
            for texture in self.textures
        ]

    def is_empty_square(self, map_x, map_y):
        if map_x < 0 or map_x >= self.width:
            return False
        if map_y < 0 or map_y >= self.height:
            return False
        return self.squares[map_x][map_y] == 0

    def _square_color(self, square):
        if square == 1:
            return YELLOW
        elif square == 2:
            return BLUE

    def raycast(self, surface, loc, dir, plane):
        width, height = surface.get_width(), surface.get_height()

        # TODO: Let the user of this method handle the buffer?
        # buffer = pg.Surface((width, height))
        # buffer_pixels = pg.PixelArray(buffer)

        # TODO: Read more about pygame's PixelArray object.
        surface_pixels = pg.PixelArray(surface)

        for x in range(width):
            camera_x = 2 * x / width - 1
            ray_dir_x = dir[0] + camera_x * plane[0]
            ray_dir_y = dir[1] + camera_x * plane[1]

            if ray_dir_y == 0:
                x_rate = 0
            elif ray_dir_x == 0:
                x_rate = 1
            else:
                x_rate = abs(1 / ray_dir_x)

            if ray_dir_x == 0:
                y_rate = 0
            elif ray_dir_y == 0:
                y_rate = 1
            else:
                y_rate = abs(1 / ray_dir_y)

            map_x, map_y = int(loc[0]), int(loc[1])
            if ray_dir_x < 0:
                x_offset = (loc[0] - map_x) * x_rate
                x_step = -1
            else:
                x_offset = ((map_x + 1) - loc[0]) * x_rate
                x_step = 1

            if ray_dir_y < 0:
                y_offset = (loc[1] - map_y) * y_rate
                y_step = -1
            else:
                y_offset = ((map_y + 1) - loc[1]) * y_rate
                y_step = 1

            while True:
                if x_offset < y_offset:
                    x_offset += x_rate
                    map_x += x_step
                    side = 'x'
                else:
                    y_offset += y_rate
                    map_y += y_step
                    side = 'y'

                square = self.squares[map_x][map_y]
                if square > 0:
                    break

            # Note: `texture_x' always satisfies 0 <= wall_x < self.texture_size
            if side == 'x':
                wall_dist = (map_x - loc[0] + (1 - x_step) / 2) / ray_dir_x
                wall_x = loc[1] + wall_dist * ray_dir_y
                wall_x -= math.floor(wall_x)
                texture_x = int(wall_x * self.texture_size)
                if ray_dir_x > 0:
                    texture_x = self.texture_size - texture_x - 1
            elif side == 'y':
                wall_dist = (map_y - loc[1] + (1 - y_step) / 2) / ray_dir_y
                wall_x = loc[0] + wall_dist * ray_dir_x
                wall_x -= math.floor(wall_x)
                texture_x = int(wall_x * self.texture_size)
                if ray_dir_y < 0:
                    texture_x = self.texture_size - texture_x - 1
            else:
                # TODO: Error.
                pass

            # + small value in denominator to prevent division by zero
            line_height = int(height / (wall_dist + 0.1))

            y_start = int((height - line_height) / 2)
            if y_start < 0:
                y_start = 0

            y_end = int((height + line_height) / 2)
            if y_end >= height:
                y_end = height - 1

            texture = self.textures[square-1]
            texture_pixels = self.texture_pixels[square-1]

            y_step = self.texture_size / line_height
            # y_pos = (y_start - (height - line_height) / 2) * y_step
            y_pos = 0
            for y in range(y_start, y_end):
                texture_y = int(y_pos) % self.texture_size
                y_pos += y_step
                color = texture_pixels[texture_x, texture_y]
                color = texture.unmap_rgb(color)
                if side == 'y':
                    color = (color[0] / 2, color[1] / 2, color[2] / 2, color[3])
                surface_pixels[x, y] = color

        surface_pixels.close()

        # surface.blit(buffer, (0, 0))

    def draw(self, screen, player):
        size = 20

        width, height = screen.get_width(), screen.get_height()

        # Player location relative to center of screen.
        player_x = round(player.loc[0] * size - width // 2)
        player_y = round(player.loc[1] * size - height // 2)

        for i, row in enumerate(self.squares):
            for j, square in enumerate(row):
                square_rect = pg.Rect(i * size, j * size, size, size)
                square_rect.move_ip(-player_x, -player_y)
                if square > 0:
                    color = self._square_color(square)
                    pg.draw.rect(screen, color, square_rect)

        start = (width // 2, height // 2)
        end = (
            round(start[0] + 10 * player.dir[0]),
            round(start[1] + 10 * player.dir[1])
        )
        pg.draw.line(screen, WHITE, start, end)

class Player:
    def __init__(self, loc, dir, fov=math.pi / 2):
        self.loc = loc
        self.dir = normalize(dir)
        self.fov = fov
        self.plane = rotate(self.dir, math.pi / 2)
        self.plane[0] *= abs(math.tan(self.fov / 2))
        self.plane[1] *= abs(math.tan(self.fov / 2))

        self.turning_left = False
        self.turning_right = False

        self.moving_forward = False
        self.moving_backward = False

        self.velocity = 0

    def move(self, map):
        disp = (self.dir[0] * self.velocity, self.dir[1] * self.velocity)

        map_x = int(self.loc[0] + disp[0])
        map_y = int(self.loc[1])
        if map.is_empty_square(map_x, map_y):
            self.loc[0] += disp[0]

        map_x = int(self.loc[0])
        map_y = int(self.loc[1] + disp[1])
        if map.is_empty_square(map_x, map_y):
            self.loc[1] += disp[1]

    def turn(self, angle):
        self.dir = rotate(self.dir, angle)
        self.plane = rotate(self.dir, math.pi / 2)
        self.plane[0] *= abs(math.tan(self.fov / 2))
        self.plane[1] *= abs(math.tan(self.fov / 2))

if __name__ == '__main__':
    pg.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    # SCREEN_WIDTH, SCREEN_HEIGHT = 320, 200
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    FPS = 60
    clock = pg.time.Clock()

    map = Map()
    # player = Player([2, 2], [1, 1], 66 / (2 * math.pi))
    player = Player([10, 2], [1, 1])

    showing_map = False

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_LEFT:
                    player.turning_left = True
                elif event.key == pg.K_RIGHT:
                    player.turning_right = True
                elif event.key == pg.K_UP:
                    player.moving_forward = True
                elif event.key == pg.K_DOWN:
                    player.moving_backward = True
                elif event.key == pg.K_TAB:
                    showing_map = not showing_map
            elif event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    player.turning_left = False
                elif event.key == pg.K_RIGHT:
                    player.turning_right = False
                elif event.key == pg.K_UP:
                    player.moving_forward = False
                elif event.key == pg.K_DOWN:
                    player.moving_backward = False
            elif event.type == pg.QUIT:
                running = False

        if player.turning_left:
            player.turn(-1 / (6 * math.pi))
        if player.turning_right:
            player.turn(1 / (6 * math.pi))

        player.velocity -= 0.5 * player.velocity
        if player.moving_forward or player.moving_backward:
            if player.moving_forward:
                player.velocity = 0.1
            elif player.moving_backward:
                player.velocity = -0.1

        player.move(map)

        screen.fill(BLACK)

        if showing_map:
            # screen.fill(BLACK)
            map.draw(screen, player)
        else:
            map.raycast(screen, player.loc, player.dir, player.plane)

        pg.display.flip()
        clock.tick(FPS)

    pg.quit()
