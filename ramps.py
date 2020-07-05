import pygame as pg

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

TILE_WIDTH, TILE_HEIGHT = 32, 32

class Map:
    def __init__(self, player, blocks, ramps):
        self.player = player
        self.blocks = blocks
        self.ramps = ramps

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

        self.x, self.y = self.rect.topleft

    def move(self, disp, blocks, ramps):
        self.rect.x = round(self.rect.x + disp[0])
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if disp[0] > 0:
                    self.rect.right = block.rect.left
                elif disp[0] < 0:
                    self.rect.left = block.rect.right
        self.x = self.rect.x

        self.rect.y = round(self.rect.y + disp[1])
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if disp[1] > 0:
                    self.rect.bottom = block.rect.top
                elif disp[1] < 0:
                    self.rect.top = block.rect.bottom
        self.y = self.rect.y

class Block(pg.sprite.Sprite):
    def __init__(self, loc, surface_type=None):
        super().__init__()
        self.image = pg.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.rect = self.image.get_rect(
            topleft=(loc[0] * TILE_WIDTH, loc[1] * TILE_HEIGHT)
        )

        if surface_type is None:
            self.image.fill(WHITE)

class Ramp(pg.sprite.Sprite):
    def __init__(self, loc, size, ramp_type, surface_type=None):
        super().__init__()
        width, height = TILE_WIDTH * size[0], TILE_HEIGHT * size[1]
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect(
            topleft=(loc[0] * TILE_WIDTH, loc[1] * TILE_HEIGHT)
        )

        if surface_type is None:
            if ramp_type == 'left_ramp':
                points = ((0, 0), (0, width-1), (width-1, height-1))
                pg.draw.polygon(self.image, WHITE, points)
            elif ramp_type == 'right_ramp':
                points = ((0, height-1), (width-1, height-1), (width-1, 0))
                pg.draw.polygon(self.image, WHITE, points)

if __name__ == '__main__':
    pg.init()

    FPS = 60
    SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    player = Player((3, 4))
    blocks = [Block((x, 10)) for x in range(10)]
    ramps = []

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
            elif event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    player.moving_left = False
                elif event.key == pg.K_RIGHT:
                    player.moving_right = False
            elif event.type == pg.QUIT:
                running = False

        disp = [0, 0]
        if player.moving_left:
            disp[0] -= 5
        if player.moving_right:
            disp[0] += 5
        player.move(disp, blocks, ramps)

        screen.fill(BLACK)

        for block in blocks:
            screen.blit(block.image, block.rect)

        screen.blit(player.image, player.rect)

        pg.display.flip()
        clock.tick(FPS)

    pg.quit()
