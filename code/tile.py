import pygame
from settings import *

HITBOX_OFFSET = {
    'player': -26,
    'object': -40,
    'grass': -10,
    'invisible': 0,
    'floor': 0,
    'decor': 0
}

Z_INDEX = {
    'floor': 0,
    'decor': 1,
    'player': 2,
    'grass': 3,
    'object': 4
}

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=None):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface if surface else pygame.Surface((TILESIZE, TILESIZE))

        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)

        y_offset = HITBOX_OFFSET.get(sprite_type, 0)
        self.hitbox = self.rect.inflate(0, y_offset)
        self.z_index = Z_INDEX.get(sprite_type, 1)


