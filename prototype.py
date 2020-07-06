import pygame as pg
import json

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

TILE_WIDTH, TILE_HEIGHT = 32, 32

class Map:
    def __init__(self, player=None, blocks=None, ramps=None, filepath=None):
        self.player = player
        self.blocks = blocks
        self.ramps = ramps

        if filepath is not None:
            self.from_file(filepath)

    def from_file(self, filepath):
        with open(filepath) as f:
            map_data = json.load(f)

        self.player = Player(**map_data['player'])

        block_data = self._compute_collision_edges(map_data['blocks'])
        self.blocks = [Block(**bd) for bd in block_data]

        # TODO: Worth doing this for ramps?
        ramp_data = self._compute_collision_edges(map_data['ramps'])
        self.ramps = [Ramp(**rd) for rd in ramp_data]

    def _compute_collision_edges(self, data_list):
        loc_dict = {tuple(data['loc']): data for data in data_list}

        for loc in loc_dict.keys():
            data = loc_dict[loc]
            if data['collision_edges'] is None:
                x, y = loc
                collision_edges = []
                if (x-1, y) not in loc_dict:
                    collision_edges.append('left')
                if (x+1, y) not in loc_dict:
                    collision_edges.append('right')
                if (x, y-1) not in loc_dict:
                    collision_edges.append('top')
                if (x, y+1) not in loc_dict:
                    collision_edges.append('bottom')
                data['collision_edges'] = collision_edges

        return loc_dict.values()

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
                if disp[0] > 0:
                    self.vx = 0
                    self.rect.right = block.rect.left
                elif disp[0] < 0:
                    self.vx = 0
                    self.rect.left = block.rect.right

        self.rect.y = round(self.rect.y + disp[1])
        self.standing_surface = None
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if disp[1] > 0:
                    self.vy = 0
                    self.rect.bottom = block.rect.top
                    self.standing_surface = block
                    self.jumping = False
                    self.jumps_left = 2
                elif disp[1] < 0:
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
                y_offset = max(y_offset, 0)  # TODO: Could this ever happen?

                if self.rect.bottom > ramp.rect.bottom - y_offset:
                    self.vy = 0
                    self.rect.bottom = int(ramp.rect.bottom - y_offset)
                    self.standing_surface = ramp
                    self.jumping = False
                    self.jumps_left = 2

        self.x, self.y = self.rect.topleft

# TODO: Only allow blocks/ramps to be hit from certain sides?

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
    def __init__(self, loc, size, ramp_type, surface_type=None,
                 collision_edges=['left', 'right', 'top', 'bottom']):
        super().__init__()
        width, height = TILE_WIDTH * size[0], TILE_HEIGHT * size[1]
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect(
            topleft=(loc[0] * TILE_WIDTH, loc[1] * TILE_HEIGHT)
        )

        self.loc = loc
        self.collision_edges = collision_edges
        self.ramp_type = ramp_type

        if surface_type is None:
            if self.ramp_type == 'left_ramp':
                points = ((0, 0), (0, width-1), (width-1, height-1))
                pg.draw.polygon(self.image, WHITE, points)
            elif self.ramp_type == 'right_ramp':
                points = ((0, height-1), (width-1, height-1), (width-1, 0))
                pg.draw.polygon(self.image, WHITE, points)

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

if __name__ == '__main__':
    pg.init()

    FPS = 60
    # SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    map = Map(filepath='map.json')
    player = map.player
    blocks = map.blocks
    ramps = map.ramps

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

        for block in blocks:
            screen.blit(block.image, block.rect)

        for ramp in ramps:
            screen.blit(ramp.image, ramp.rect)

        screen.blit(player.image, player.rect)

        pg.display.flip()
        clock.tick(FPS)

    pg.quit()
