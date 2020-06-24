import pygame as pg
from player import Player
from tile import Tile
from map import Map
from viewport import Viewport

def main():
    pg.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    # SCREEN_WIDTH = 600
    # SCREEN_HEIGHT = 480

    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    with open('map.txt') as f:
        string_rep = [line.rstrip() for line in f]
        map = Map(string_rep, 40, (25, 50), 1.5)

    viewport = Viewport(screen, map)

    player = map.get_player()
    tiles = map.get_tiles()
    sprites = tiles + [player]

    bg_image = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_image.fill((0, 255, 0))
    bg_rect = bg_image.get_rect(topleft=(0, round(0.75 * SCREEN_HEIGHT)))

    cloud_image1 = pg.Surface((60, 60))
    cloud_image1.fill((100, 100, 100))
    cloud_rect1 = cloud_image1.get_rect(topleft=(100, 200))

    cloud_image2 = pg.Surface((100, 100))
    cloud_image2.fill((120, 120, 120))
    cloud_rect2 = cloud_image2.get_rect(topleft=(300, 50))

    # TODO: If too small, can mess up collision detection. Could "rectify" by
    # increasing gravity to compensate.
    # TODO: Might just want to get rid of time delta.
    dt = 1.0  # Time delta per frame

    clock = pg.time.Clock()

    running = True
    while running:
        print(player.vx, player.vy)
        # print(player.standing_tile)

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_UP:
                    player.jump()
                elif event.key == pg.K_LEFT:
                    player.start_walking_left()
                elif event.key == pg.K_RIGHT:
                    player.start_walking_right()
            elif event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    player.stop_walking_left()
                elif event.key == pg.K_RIGHT:
                    player.stop_walking_right()
            elif event.type == pg.QUIT:
                running = False

        if pg.key.get_mods() & pg.KMOD_SHIFT:
            player.start_running()
        else:
            player.stop_running()

        player.physics_step(dt)

        screen.fill((0, 0, 0))

        screen.blit(bg_image, bg_rect)

        # TODO: Parallax logic needs to be put into viewport class.
        old_x = viewport.rect.x
        viewport.update(player)
        new_x = viewport.rect.x
        cloud_rect1.x = round(cloud_rect1.x + 0.25 * (new_x - old_x))
        cloud_rect2.x = round(cloud_rect2.x + 0.5 * (new_x - old_x))

        screen.blit(cloud_image1, cloud_rect1)
        screen.blit(cloud_image2, cloud_rect2)

        viewport.draw(sprites)
        pg.display.flip()

        clock.tick(60)

    pg.quit()

if __name__ == '__main__':
    main()
