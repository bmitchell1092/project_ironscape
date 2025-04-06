import pygame
from settings import *

# Adjust vertical collision box offset based on tile type
HITBOX_OFFSET = {
    'player': -26,
    'object': -40,
    'grass': -10,
    'invisible': 0,
    'floor': 0,
    'decor': 0
}

# Rendering order: higher numbers draw on top
Z_INDEX = {
    'floor': 0,
    'decor': 0,
    'player': 2,
    'grass': 0,
    'object': 4
}

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=None):
        super().__init__(groups)
        self.sprite_type = sprite_type

        # Default surface if not provided
        self.image = surface if surface else pygame.Surface((TILESIZE, TILESIZE))

        # Object tiles are offset up visually
        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)

        # Hitbox adjustment for collision handling
        y_offset = HITBOX_OFFSET.get(sprite_type, 0)
        self.hitbox = self.rect.inflate(0, y_offset)

        # Assign a rendering order (if you ever need it)
        self.z_index = Z_INDEX.get(sprite_type, 1)



