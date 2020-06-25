
class BackgroundLayer:
    def __init__(self, sprites, parallax_factors=(1.0, 1.0)):
        self.sprites = sprites
        self.parallax_factors = parallax_factors

    def get_sprites(self):
        return self.sprites

    def get_parallax_factors(self):
        return self.parallax_factors
