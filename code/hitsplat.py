# hitsplat.py
import pygame
from support import get_asset_path

class Hitsplat(pygame.sprite.Sprite):
    def __init__(self, pos, damage, groups):
        super().__init__(groups)
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)  # Invisible placeholder
        self.rect = self.image.get_rect(center=pos)

        self.damage = damage
        self.creation_time = pygame.time.get_ticks()
        self.lifetime = 0  # Disabled by default

    def update(self):
        self.kill()

    def draw(self, surface):
        pass
