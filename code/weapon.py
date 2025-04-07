# weapon.py (direction-based weapon positioning with x/y offsets)
import pygame
import os
from support import get_asset_path

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.player = player
        self.direction = player.status.split('_')[0]

        # Per-direction x/y offsets (relative to player center)
        self.offset_map = {
            'up': (0, -40),
            'down': (0, 40),
            'left': (-40, 10),
            'right': (40, 10)
        }

        # Load correct weapon image (default: sword)
        weapon_path = get_asset_path('graphics', 'weapons', 'sword', f'{self.direction}.png')
        if not os.path.exists(weapon_path):
            print(f"[ERROR] Weapon image not found: {weapon_path}")
            self.image = pygame.Surface((32, 32))  # fallback visual
        else:
            self.image = pygame.image.load(weapon_path).convert_alpha()

        self.rect = self.image.get_rect()
        self.z_index = 3  # Ensure weapon is drawn above the player
        self.update_position()

        # Optional animation placeholders
        self.frame_index = 0
        self.animation_speed = 0.2
        self.frames = [self.image]

    def update_position(self):
        center_x, center_y = self.player.rect.center
        offset_x, offset_y = self.offset_map.get(self.direction, (0, 0))
        self.rect.center = (center_x + offset_x, center_y + offset_y)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
        self.update_position()






