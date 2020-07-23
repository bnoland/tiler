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
            [1,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,2,2,2,2,0,0,0,0,2,0,2,0,2,0,0,0,1],
            [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,2,0,-1,0,2,0,0,0,1],
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
            [1,1,0,0,0,0,-1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]

        self.width = len(self.squares)
        self.height = len(self.squares[0])

        # TODO: In general might want to do texture loading *outside* of the map
        # class.
        self.textures = [
            pg.image.load('marble_color.png').convert(),
            pg.image.load('cloud_color.png').convert()
        ]

        self.texture_size = 64  # Fixed for now.

        self.lighting_list = [
            self.compute_lighting((map_x, map_y))
            for map_x, row in enumerate(self.squares)
            for map_y, square in enumerate(row)
            if square == -1
        ]

    def compute_lighting(self, light_loc):
        lighting = {}
        for i in range(0, 360*100):
            angle = i / (200 * math.pi)
            ray_dir = (math.cos(angle), math.sin(angle))

            map_x, map_y, wall_dist, side, texture_x = \
                self.cast_ray(light_loc, ray_dir)

            if not (map_x, map_y) in lighting:
                lighting[(map_x, map_y)] = {
                    'left': {},
                    'right': {},
                    'top': {},
                    'bottom': {}
                }

            if side == 'x':
                if ray_dir[0] > 0:
                    lighting_data = lighting[(map_x, map_y)]['left']
                    lighting_data[texture_x] = wall_dist
                else:
                    lighting_data = lighting[(map_x, map_y)]['right']
                    lighting_data[texture_x] = wall_dist
            elif side == 'y':
                if ray_dir[1] > 0:
                    lighting_data = lighting[(map_x, map_y)]['top']
                    lighting_data[texture_x] = wall_dist
                else:
                    lighting_data = lighting[(map_x, map_y)]['bottom']
                    lighting_data[texture_x] = wall_dist

        return lighting

    def is_empty_square(self, map_x, map_y):
        if map_x < 0 or map_x >= self.width:
            return False
        if map_y < 0 or map_y >= self.height:
            return False
        return self.squares[map_x][map_y] <= 0

    # TODO: How to associate this with the *class* instead of the *object*?
    def _square_color(self, square):
        if square == 1:
            return YELLOW
        elif square == 2:
            return BLUE

    def cast_ray(self, start_loc, ray_dir):
        if ray_dir[1] == 0:
            x_rate = 0
        elif ray_dir[0] == 0:
            x_rate = 1
        else:
            x_rate = abs(1 / ray_dir[0])

        if ray_dir[0] == 0:
            y_rate = 0
        elif ray_dir[1] == 0:
            y_rate = 1
        else:
            y_rate = abs(1 / ray_dir[1])

        map_x, map_y = int(start_loc[0]), int(start_loc[1])
        if ray_dir[0] < 0:
            x_offset = (start_loc[0] - map_x) * x_rate
            x_step = -1
        else:
            x_offset = ((map_x + 1) - start_loc[0]) * x_rate
            x_step = 1

        if ray_dir[1] < 0:
            y_offset = (start_loc[1] - map_y) * y_rate
            y_step = -1
        else:
            y_offset = ((map_y + 1) - start_loc[1]) * y_rate
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
            wall_dist = (map_x - start_loc[0] + (1 - x_step) / 2) / ray_dir[0]
            wall_x = start_loc[1] + wall_dist * ray_dir[1]
            wall_x -= math.floor(wall_x)
            texture_x = int(wall_x * self.texture_size)
            if ray_dir[0] > 0:
                texture_x = self.texture_size - texture_x - 1
        elif side == 'y':
            wall_dist = (map_y - start_loc[1] + (1 - y_step) / 2) / ray_dir[1]
            wall_x = start_loc[0] + wall_dist * ray_dir[0]
            wall_x -= math.floor(wall_x)
            texture_x = int(wall_x * self.texture_size)
            if ray_dir[1] < 0:
                texture_x = self.texture_size - texture_x - 1

        return (map_x, map_y, wall_dist, side, texture_x)

    def render(self, surface, loc, dir, plane):
        width, height = surface.get_width(), surface.get_height()

        for x in range(width):
            camera_x = 2 * x / width - 1
            ray_dir = (
                dir[0] + camera_x * plane[0],
                dir[1] + camera_x * plane[1]
            )

            map_x, map_y, wall_dist, side, texture_x = \
                self.cast_ray(loc, ray_dir)

            # + small value in denominator to prevent division by zero
            line_height = int(height / (wall_dist + 0.1))

            y_start = int((height - line_height) / 2)
            if y_start < 0:
                y_start = 0

            square = square = self.squares[map_x][map_y]
            texture = self.textures[square-1]

            texture_buffer = pg.Surface(texture.get_size())
            texture_buffer.blit(
                texture, (0, 0), (texture_x, 0, 1, self.texture_size))
            texture_buffer = pg.transform.scale(
                texture_buffer, (1, round(line_height)))

            surface.blit(texture_buffer, (x, y_start))

            orig_dim_factor = 1 - 1 / (wall_dist + 0.1)
            dim_factor = orig_dim_factor

            # Adjust texture dim factor based on light sources.
            for lighting in self.lighting_list:
                if (map_x, map_y) in lighting:
                    if side == 'x':
                        if ray_dir[0] > 0:
                            lighting_data = lighting[(map_x, map_y)]['left']
                        else:
                            lighting_data = lighting[(map_x, map_y)]['right']
                    elif side == 'y':
                        if ray_dir[1] > 0:
                            lighting_data = lighting[(map_x, map_y)]['top']
                        else:
                            lighting_data = lighting[(map_x, map_y)]['bottom']

                    if texture_x in lighting_data:
                        wall_dist = lighting_data[texture_x]
                        # dim_factor *= wall_dist / 10
                        dim_factor = min(wall_dist / 10, dim_factor)
                        if dim_factor > orig_dim_factor:
                            dim_factor = orig_dim_factor

            if dim_factor > 1:
                dim_factor = 1
            if dim_factor < 0:
                dim_factor = 0

            darken = pg.Surface(texture_buffer.get_size()).convert_alpha()
            darken.fill((0, 0, 0, 255 * dim_factor))  # Darkness
            surface.blit(darken, (x, y_start))

    def draw(self, screen, player):
        size = 20

        width, height = screen.get_width(), screen.get_height()

        # Player location relative to center of screen.
        player_x = round(player.loc[0] * size - width // 2)
        player_y = round(player.loc[1] * size - height // 2)

        for map_x, row in enumerate(self.squares):
            for map_y, square in enumerate(row):
                square_rect = pg.Rect(map_x * size, map_y * size, size, size)
                square_rect.move_ip(-player_x, -player_y)
                if square > 0:
                    color = self._square_color(square)
                    pg.draw.rect(screen, color, square_rect)

                # Indicate squares affected by lighting.
                for lighting in self.lighting_list:
                    if (map_x, map_y) in lighting.keys():
                        pg.draw.rect(screen, GREEN, square_rect)

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

        gap_size = 0.15

        if disp[0] != 0:
            gap_x = math.copysign(gap_size, disp[0])
            map_x = int(self.loc[0] + disp[0] + gap_x)
            map_y = int(self.loc[1])
            if map.is_empty_square(map_x, map_y):
                self.loc[0] += disp[0]

        if disp[1] != 0:
            gap_y = math.copysign(gap_size, disp[1])
            map_x = int(self.loc[0])
            map_y = int(self.loc[1] + disp[1] + gap_y)
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
            map.draw(screen, player)
        else:
            map.render(screen, player.loc, player.dir, player.plane)

        pg.display.flip()
        clock.tick(FPS)

    pg.quit()
