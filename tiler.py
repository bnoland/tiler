import pygame as pg
from player import Player
from tile import Tile
from map import Map
from viewport import Viewport

def main():
    pg.init()

    # SCREEN_WIDTH = 800
    # SCREEN_HEIGHT = 600

    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 480

    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    with open('map.txt') as f:
        string_rep = [line.rstrip() for line in f]
        map = Map(string_rep, (32, 32), (25, 50))

    viewport = Viewport(screen, map)

    player = map.get_player()
    tiles = map.get_tiles()
    sprites = tiles + [player]

    bg_image = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_image.fill((0, 255, 0))
    bg_rect = bg_image.get_rect(topleft=(0, round(0.75 * SCREEN_HEIGHT)))

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

        screen.blit(bg_image, bg_rect)

        viewport.update(player)
        viewport.draw(sprites)

        pg.display.flip()
        clock.tick(60)

    pg.quit()

if __name__ == '__main__':
    main()
