# melee.py
import pygame
import os
from support import get_asset_path, import_folder
from item import get_item_data

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.player = player
        self.direction = player.status.split('_')[0]

        # Determine equipped weapon
        weapon_id = self.player.equipment.get_equipped_items("Weapon")
        self.weapon_item = get_item_data(weapon_id) if weapon_id else None
        self.subtype = self.weapon_item.get("subtype", "unarmed") if self.weapon_item else "unarmed"

        # Build path to directional animation folder
        weapon_dir = get_asset_path("graphics", "weapons", self.subtype, self.direction)
        if os.path.exists(weapon_dir):
            self.frames = import_folder(weapon_dir)
        else:
            print(f"[WARNING] Weapon animation folder not found: {weapon_dir}")
            self.frames = []

        self.frame_index = 0
        self.animation_speed = 0.2
        self.image = self.frames[0] if self.frames else pygame.Surface((32, 32))
        self.rect = self.image.get_rect()
        self.z_index = 3

        # Offset for weapon position based on facing
        offset_map = {
            'up': (0, -40),
            'down': (0, 40),
            'left': (-40, 10),
            'right': (40, 10)
        }
        self.offset = offset_map.get(self.direction, (0, 0))
        self.update_position()

    def update_position(self):
        center_x, center_y = self.player.rect.center
        offset_x, offset_y = self.offset
        self.rect.center = (center_x + offset_x, center_y + offset_y)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = len(self.frames) - 1  # Hold last frame
        if self.frames:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
        self.update_position()













