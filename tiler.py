import pygame as pg
from player import Player
from tile import Tile
from map import Map
from viewport import Viewport
from background import BackgroundLayer

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

    player = map.get_player()
    tiles = map.get_tiles()
    sprites = tiles + [player]

    bg_image = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_image.fill((0, 255, 0))
    bg_rect = bg_image.get_rect(topleft=(0, round(0.75 * SCREEN_HEIGHT)))

    # TODO: If too small, can mess up collision detection. Could "rectify" by
    # increasing gravity to compensate.
    # TODO: Might just want to get rid of time delta.
    dt = 1.0  # Time delta per frame

    viewport = Viewport(screen, map)
    player.physics_step(dt)  # Ensure player position is kosher
    viewport.center_on(player)

    # Hacky parallax demo.
    from tile import EarthTile
    import random
    cloud_tiles1 = [
        EarthTile((200*x, 200+100*(random.random()-0.5)), 50)
        for x in range(1, 10)]
    cloud_tiles2 = [
        EarthTile((150*x, 200+150*(random.random()-0.5)), 30)
        for x in range(1, 10)]
    map.background_layers = [
        BackgroundLayer(cloud_tiles1, (0.25, 0.25)),
        BackgroundLayer(cloud_tiles2, (0.5, 0.5))]

    clock = pg.time.Clock()

    running = True
    while running:
        # print(player.vx, player.vy)
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

        # TODO: May want to move blitting stuff to start of game loop if we
        # perform any sprite updates before the loop begins.
        screen.fill((0, 0, 0))

        screen.blit(bg_image, bg_rect)

        viewport.update(player)
        viewport.draw(cloud_tiles2)
        viewport.draw(cloud_tiles1)
        viewport.draw(sprites)

        pg.display.flip()

        clock.tick(60)

    pg.quit()

if __name__ == '__main__':
    main()
