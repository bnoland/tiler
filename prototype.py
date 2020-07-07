import pygame as pg
import json

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

TILE_WIDTH, TILE_HEIGHT = 32, 32

class Map:
    def __init__(self, size=None, player=None, blocks=None, ramps=None,
                 filepath=None):
        if filepath is None:
            width, height = TILE_WIDTH * size[0], TILE_HEIGHT * size[1]
            self.rect = pg.Rect((0, 0), (width, height))

            self.player = player
            self.blocks = blocks
            self.ramps = ramps
        else:
            self._from_file(filepath)

        # Mainly for debugging.
        self.border = pg.sprite.Sprite()
        self.border.image = pg.Surface(self.rect.size)
        self.border.rect = self.border.image.get_rect()
        pg.draw.rect(self.border.image, RED, self.border.rect, 1)
        self.border.image.set_colorkey(BLACK)

    def _from_file(self, filepath):
        with open(filepath) as f:
            map_data = json.load(f)

        size = map_data['size']
        width, height = TILE_WIDTH * size[0], TILE_HEIGHT * size[1]
        self.rect = pg.Rect((0, 0), (width, height))

        player_data = map_data['player']
        self.player = Player(**player_data)

        block_data_list = self._compute_block_collision_edges(map_data)
        self.blocks = [Block(**d) for d in block_data_list]

        ramp_data_list = map_data['ramps']
        self.ramps = [Ramp(**d) for d in ramp_data_list]

    def _compute_block_collision_edges(self, map_data):
        block_dict = {tuple(data['loc']): data
                      for data in map_data['blocks']}
        ramp_dict = {tuple(data['loc']): data
                     for data in map_data['ramps']}

        open_tile = lambda x, y: (x, y) not in block_dict and \
                                 (x, y) not in ramp_dict

        for loc in block_dict.keys():
            data = block_dict[loc]
            if data['collision_edges'] is None:
                x, y = loc
                collision_edges = []
                if open_tile(x - 1, y):
                    collision_edges.append('left')
                if open_tile(x + 1, y):
                    collision_edges.append('right')
                if open_tile(x, y - 1):
                    collision_edges.append('top')
                if open_tile(x, y + 1):
                    collision_edges.append('bottom')
                data['collision_edges'] = collision_edges

        return block_dict.values()

class Viewport:
    def __init__(self, loc, pixel_size):
        self.rect = pg.Rect(loc, pixel_size)

    def update(self, sprite, map):
        snap_rate = 1 / 1.1  # If zero will immediately snap on sprite.
        new_center = [0, 0]
        new_center[0] = sprite.rect.center[0] + \
            (self.rect.center[0] - sprite.rect.center[0]) * snap_rate
        new_center[1] = sprite.rect.center[1] + \
            (self.rect.center[1] - sprite.rect.center[1]) * snap_rate

        self.rect.center = round(new_center[0]), round(new_center[1])

        if self.rect.left < map.rect.left:
            self.rect.left = map.rect.left
        if self.rect.right > map.rect.right:
            self.rect.right = map.rect.right
        if self.rect.top < map.rect.top:
            self.rect.top = map.rect.top
        if self.rect.bottom > map.rect.bottom:
            self.rect.bottom = map.rect.bottom

    def apply(self, sprite, parallax=(0, 0)):
        x, y = self.rect.topleft
        x_disp = round(-x + parallax[0] * x)
        y_disp = round(-y + parallax[1] * y)
        return sprite.rect.move((x_disp, y_disp))

    def draw(self, screen, sprite, parallax=(0, 0)):
        screen.blit(sprite.image, self.apply(sprite, parallax))

class Player(pg.sprite.Sprite):
    def __init__(self, loc):
        super().__init__()
        width, height = TILE_WIDTH, 2 * TILE_HEIGHT
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect(
            topleft=(loc[0] * TILE_WIDTH, loc[1] * TILE_HEIGHT)
        )
        self.image.fill(RED)

        self.moving_left = False
        self.moving_right = False

        self.jumping = False
        self.jumps_left = 2

        self.standing_surface = None

        self.x, self.y = self.rect.topleft
        self.vx, self.vy = 0, 0

    def move(self, disp, blocks, ramps):
        self.rect.x = round(self.rect.x + disp[0])
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if 'left' in block.collision_edges and disp[0] > 0:
                    print('left')
                    self.vx = 0
                    self.rect.right = block.rect.left
                elif 'right' in block.collision_edges and disp[0] < 0:
                    print('right')
                    self.vx = 0
                    self.rect.left = block.rect.right

        self.rect.y = round(self.rect.y + disp[1])
        self.standing_surface = None
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if 'top' in block.collision_edges and disp[1] > 0:
                    self.vy = 0
                    self.rect.bottom = block.rect.top
                    self.standing_surface = block
                    self.jumping = False
                    self.jumps_left = 2
                elif 'bottom' in block.collision_edges and disp[1] < 0:
                    self.vy = 0
                    self.rect.top = block.rect.bottom

        for ramp in ramps:
            if self.rect.colliderect(ramp.rect):
                slope = ramp.rect.height / ramp.rect.width
                if ramp.ramp_type == 'left_ramp':
                    y_offset = slope * (ramp.rect.right - self.rect.left)
                elif ramp.ramp_type == 'right_ramp':
                    y_offset = slope * (self.rect.right - ramp.rect.left)

                y_offset = min(y_offset, ramp.rect.height)
                y_offset = max(y_offset, 0)  # TODO: Needed?

                if self.rect.bottom > ramp.rect.bottom - y_offset:
                    self.vy = 0
                    self.rect.bottom = int(ramp.rect.bottom - y_offset)
                    self.standing_surface = ramp
                    self.jumping = False
                    self.jumps_left = 2

        self.x, self.y = self.rect.topleft

class Tile(pg.sprite.Sprite):
    pass

class Block(pg.sprite.Sprite):
    def __init__(self, loc, surface_type=None,
                 collision_edges=['left', 'right', 'top', 'bottom']):
        super().__init__()
        self.image = pg.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.rect = self.image.get_rect(
            topleft=(loc[0] * TILE_WIDTH, loc[1] * TILE_HEIGHT)
        )

        self.loc = loc
        self.collision_edges = collision_edges

        if surface_type is None:
            self.image.fill(WHITE)

        # For debugging.
        width, height = self.rect.size
        if 'left' in self.collision_edges:
            pg.draw.line(self.image, RED, (0, 0), (0, height-1))
        if 'right' in self.collision_edges:
            pg.draw.line(
                self.image, RED, (width-1, 0), (width-1, height-1))
        if 'top' in self.collision_edges:
            pg.draw.line(self.image, RED, (0, 0), (width-1, 0))
        if 'bottom' in self.collision_edges:
            pg.draw.line(
                self.image, RED, (0, height-1), (width-1, height-1))

class Ramp(pg.sprite.Sprite):
    def __init__(self, loc, size, ramp_type, surface_type=None):
        super().__init__()
        width, height = TILE_WIDTH * size[0], TILE_HEIGHT * size[1]
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect(
            topleft=(loc[0] * TILE_WIDTH, loc[1] * TILE_HEIGHT)
        )

        self.loc = loc
        self.ramp_type = ramp_type

        if surface_type is None:
            self.image.set_colorkey(BLACK)
            if self.ramp_type == 'left_ramp':
                points = ((0, 0), (0, width-1), (width-1, height-1))
                pg.draw.polygon(self.image, WHITE, points)
            elif self.ramp_type == 'right_ramp':
                points = ((0, height-1), (width-1, height-1), (width-1, 0))
                pg.draw.polygon(self.image, WHITE, points)

    def get_tiles(self):
        pass

if __name__ == '__main__':
    pg.init()

    FPS = 60
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    map = Map(filepath='map.json')
    player = map.player
    blocks = map.blocks
    ramps = map.ramps

    viewport = Viewport((0, 0), screen.get_rect().size)

    # player = Player((3, 4))
    #
    # blocks = []
    # blocks.extend([Block((x, 18)) for x in range(25)])
    # blocks.extend([Block((x, y)) for x in range(8, 19) for y in range(14, 18)])
    # blocks.extend([Block((x, y)) for x in range(12, 19) for y in range(12, 14)])
    #
    # ramps = [
    #     Ramp((4, 14), (4, 4), 'right_ramp'),
    #     Ramp((8, 12), (4, 2), 'right_ramp'),
    #     Ramp((12, 11), (3, 1), 'right_ramp'),
    #     Ramp((15, 11), (4, 1), 'left_ramp'),
    #     Ramp((19, 12), (4, 4), 'left_ramp')
    # ]

    clock = pg.time.Clock()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_LEFT:
                    player.moving_left = True
                elif event.key == pg.K_RIGHT:
                    player.moving_right = True
                elif event.key == pg.K_UP:
                    player.jumping = True
            elif event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    player.moving_left = False
                elif event.key == pg.K_RIGHT:
                    player.moving_right = False
            elif event.type == pg.QUIT:
                running = False

        disp = [0, 0]

        if player.standing_surface is not None:
            player.vx -= 0.9 * player.vx
            if player.moving_left:
                player.vx -= 5
            if player.moving_right:
                player.vx += 5

            if isinstance(player.standing_surface, Ramp):
                ramp = player.standing_surface
                slope = ramp.rect.height / ramp.rect.width
                if ramp.ramp_type == 'right_ramp':
                    disp[1] -= slope * player.vx
                elif ramp.ramp_type == 'left_ramp':
                    disp[1] += slope * player.vx

        player.vy += 1.5
        if player.jumping and player.jumps_left > 0:
            player.jumps_left -= 1
            player.jumping = False
            player.vy -= 20

        disp[0] += player.vx
        disp[1] += player.vy
        player.move(disp, blocks, ramps)

        screen.fill(BLACK)

        viewport.update(player, map)

        for block in blocks:
            viewport.draw(screen, block)

        for ramp in ramps:
            viewport.draw(screen, ramp)

        viewport.draw(screen, player)

        viewport.draw(screen, map.border)

        pg.display.flip()
        clock.tick(FPS)

    pg.quit()
