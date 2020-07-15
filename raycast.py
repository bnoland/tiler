import pygame as pg
import math

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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
            [1,0,0,0,0,0,2,2,2,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
            [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,3,0,0,0,3,0,0,0,1],
            [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,2,0,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,4,0,0,0,0,5,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,4,0,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]

        self.width = len(self.squares[0])
        self.height = len(self.squares)

    def is_empty_square(self, map_loc_x, map_loc_y):
        if map_loc_x < 0 or map_loc_x >= self.width:
            return False
        if map_loc_y < 0 or map_loc_y >= self.height:
            return False
        return self.squares[map_loc_x][map_loc_y] == 0

    def raycast(self, surface, loc, dir, plane):
        width, height = surface.get_width(), surface.get_height()
        for x in range(width):
            camera_x = 2 * x / width - 1
            ray_dir_x = dir[0] + camera_x * plane[0]
            ray_dir_y = dir[1] + camera_x * plane[1]

            # TODO: Apparently don't need to compute norm.
            norm = math.sqrt(ray_dir_x * ray_dir_x + ray_dir_y * ray_dir_y)
            # if ray_dir_x == 0:
            #     # Ray moving vertically
            #     rate_x = 0
            # else:
            #     rate_x = abs(norm / ray_dir_x)
            #
            # if ray_dir_y == 0:
            #     # Ray moving horizontally
            #     rate_y = 0
            # else:
            #     rate_y = abs(norm / ray_dir_y)

            # TODO: Derive this.
            if ray_dir_y == 0:
                rate_x = 0
            elif ray_dir_x == 0:
                rate_x = 1
            else:
                rate_x = abs(norm / ray_dir_x)

            if ray_dir_x == 0:
                rate_y = 0
            elif ray_dir_y == 0:
                rate_y = 1
            else:
                rate_y = abs(norm / ray_dir_y)

            map_loc_x, map_loc_y = int(loc[0]), int(loc[1])
            if ray_dir_x < 0:
                ray_loc_x = (loc[0] - map_loc_x) * rate_x
                step_x = -1
            else:
                ray_loc_x = ((map_loc_x + 1) - loc[0]) * rate_x
                step_x = 1

            if ray_dir_y < 0:
                ray_loc_y = (loc[1] - map_loc_y) * rate_y
                step_y = -1
            else:
                ray_loc_y = ((map_loc_y + 1) - loc[1]) * rate_y
                step_y = 1

            while True:
                if ray_loc_x < ray_loc_y:
                    ray_loc_x += rate_x
                    map_loc_x += step_x
                    side = 'x'
                else:
                    ray_loc_y += rate_y
                    map_loc_y += step_y
                    side = 'y'

                square = self.squares[map_loc_x][map_loc_y]
                if square > 0:
                    break

            # TODO: Derive this.
            if side == 'x':
                wall_dist = (map_loc_x - loc[0] + (1 - step_x) / 2) / ray_dir_x
            elif side == 'y':
                wall_dist = (map_loc_y - loc[1] + (1 - step_y) / 2) / ray_dir_y
            else:
                # TODO: Error.
                pass

            line_height = int(height / wall_dist)
            y_start = (height - line_height) / 2
            if y_start < 0:
                y_start = 0
            y_start = int(y_start)
            y_end = (height + line_height) / 2
            if y_end >= height:
                y_end = height - 1
            y_end = int(y_end)

            if square == 1:
                color = RED
            elif square == 2:
                color = GREEN
            elif square == 3:
                color = BLUE
            elif square == 4:
                color = WHITE
            else:
                color = (100, 100, 100)

            if side == 'y':
                color = (color[0] / 2, color[1] / 2, color[2] / 2)

            pg.draw.line(screen, color, (x, y_start), (x, y_end))

class Player:
    def __init__(self, loc, dir):
        # TODO: May want to be able to adjust the FOV.
        self.loc = loc
        self.dir = normalize(dir)
        self.plane = rotate(self.dir, math.pi / 2)

        self.turning_left = False
        self.turning_right = False

        self.moving_forward = False
        self.moving_backward = False

        self.velocity = 0

    def move(self, map):
        # if direction == 'forward':
        #     disp = (self.dir[0] / 10, self.dir[1] / 10)
        # elif direction == 'backward':
        #     disp = (-self.dir[0] / 10, -self.dir[1] / 10)

        disp = (self.dir[0] * self.velocity, self.dir[1] * self.velocity)

        map_loc_x = int(self.loc[0] + disp[0])
        map_loc_y = int(self.loc[1])
        if map.is_empty_square(map_loc_x, map_loc_y):
            self.loc[0] += disp[0]

        map_loc_x = int(self.loc[0])
        map_loc_y = int(self.loc[1] + disp[1])
        if map.is_empty_square(map_loc_x, map_loc_y):
            self.loc[1] += disp[1]

    def turn(self, angle):
        self.dir = rotate(self.dir, angle)
        self.plane = rotate(self.dir, math.pi / 2)

if __name__ == '__main__':
    pg.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    FPS = 60
    clock = pg.time.Clock()

    map = Map()
    player = Player([2, 2], [1, 1])

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

        screen.fill(BLACK)

        if player.turning_left:
            player.turn(-1 / (6 * math.pi))
        if player.turning_right:
            player.turn(1 / (6 * math.pi))

        # if player.moving_forward:
        #     player.move(map, 'forward')
        # if player.moving_backward:
        #     player.move(map, 'backward')

        player.velocity -= 0.5 * player.velocity
        if player.moving_forward or player.moving_backward:
            if player.moving_forward:
                player.velocity = 0.1
            elif player.moving_backward:
                player.velocity = -0.1

        player.move(map)

        map.raycast(screen, player.loc, player.dir, player.plane)

        # start = player.loc
        # end = (
        #     player.loc[0] + 10 * player.dir[0],
        #     player.loc[1] + 10 * player.dir[1]
        # )
        # pg.draw.line(screen, WHITE, start, end, 1)
        #
        # start = end
        # end = (
        #     start[0] + 10 * player.plane[0],
        #     start[1] + 10 * player.plane[1]
        # )
        # pg.draw.line(screen, WHITE, start, end, 1)

        pg.display.flip()
        clock.tick(FPS)

    pg.quit()
