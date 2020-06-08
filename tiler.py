import pygame as pg
from player import Player
from tile import Tile
from map import Map

def main():
    pg.init()

    # SCREEN_WIDTH = 800
    # SCREEN_HEIGHT = 600
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480

    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    map = Map([
        'xxxxxxxxxxxxxxxxxxxxxxxxx',
        'xooooooooooooooooooooooox',
        'xooooooooooooooooooooooox',
        'xooooooooooooooooooooooox',
        'xooooooooooooooooooooooox',
        'xooooooooooooooooooooooox',
        'xooooooooooooooooooooooox',
        'xooooooooooooooooooooooox',
        'xooooxxoooooooooxxoooooox',
        'xooooooooooooooooooooooox',
        'xooooooooooooooooooooooox',
        'xooooooooooooooooooooooox',
        'xooooooooooooooooooooooox',
        'xooooooooooooooooooooooox',
        'xoooooxxooooooooxxxxxxxxx',
        'xooooooooooooooooooooooox',
        'xooooooooooxxxxxxooooooox',
        'xooooooooooooooooooooooox',
        'xooooooooooooooooooooooox',
        'xxxxxxxxxxxxxxxxxxxxxxxxx',
    ], (32, 30))

    player = Player(screen, map.get_tile_group(), (100, 100))
    players = pg.sprite.Group(player)

    dt = 1  # Time delta per frame

    clock = pg.time.Clock()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_UP:
                    player.jump()
            elif event.type == pg.QUIT:
                running = False

        pressed_keys = pg.key.get_pressed()
        mods = pg.key.get_mods()
        player.handle_horizontal_movement(pressed_keys, mods)
        player.physics_step(dt)

        screen.fill((0, 0, 0))

        players.draw(screen)
        map.draw(screen)

        pg.display.flip()
        clock.tick(30)

    pg.quit()

if __name__ == '__main__':
    main()
