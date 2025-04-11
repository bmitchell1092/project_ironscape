# weapon.py (direction-based weapon positioning & animation only)
import pygame
import os
from support import get_asset_path
from item import get_item_data

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.player = player
        self.direction = player.status.split('_')[0]

        # Offset for weapon position based on facing
        offset_map = {
            'up': (0, -40),
            'down': (0, 40),
            'left': (-40, 10),
            'right': (40, 10)
        }

        self.offset = offset_map.get(self.direction, (0, 0))

        # Determine equipped weapon
        weapon_id = self.player.equipment.get_equipped_items("Weapon")
        self.weapon_item = get_item_data(weapon_id) if weapon_id else None
        self.subtype = self.weapon_item.get("subtype") if self.weapon_item else "sword"

        # Fallback to a default sprite if missing
        direction_path = get_asset_path("graphics", "weapons", self.subtype, f"{self.direction}.png")
        if os.path.exists(direction_path):
            self.image = pygame.image.load(direction_path).convert_alpha()
        else:
            print(f"[WARNING] Weapon sprite not found: {direction_path}")
            self.image = pygame.Surface((32, 32))  # fallback

        self.rect = self.image.get_rect()
        self.z_index = 3
        self.update_position()

        # Optional animation logic
        self.frame_index = 0
        self.animation_speed = 0.2
        self.frames = [self.image]  # Later: allow multiple frames for animation

    def update_position(self):
        center_x, center_y = self.player.rect.center
        offset_x, offset_y = self.offset
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








