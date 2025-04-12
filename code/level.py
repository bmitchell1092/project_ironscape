# level.py
import pygame
import os
from settings import *
from tile import Tile
from player import Player
from ui import UI
from camera import YSortCameraGroup
from enemy import Enemy
from enemy import monster_data
from combat import CombatHandler
from support import import_csv_layout, cut_graphics_from_sheet, get_asset_path
from equipment import Equipment


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # Sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # Map loading
        self.create_map()

        # CHANGED: Remove AnimationPlayer usage
        # self.animation_player = AnimationPlayer()

        # CHANGED: No longer pass animation_player to Player
        self.equipment = Equipment()
        self.player = Player(
            (1792, 388),
            self.obstacle_sprites,
            self.visible_sprites,       # sprite_group
            self.visible_sprites,
            self.equipment        # groups (if you need the same group),          # equipment
        )
        self.visible_sprites.add(self.player)
        self.visible_sprites.set_camera_target(self.player)
        self.ui = UI(self.player, self.equipment)

        # Combat handler (connects player attacks to enemies)
        self.combat_handler = CombatHandler(self.player, self.enemy_sprites)
        self.player.combat_handler = self.combat_handler

    def create_map(self):
        layout_files = {
            'floor': get_asset_path('map', 'map_Floor.csv'),
            'blocks': get_asset_path('map', 'map_FloorBlocks.csv'),
            'objects': get_asset_path('map', 'map_Objects.csv'),
            'grass': get_asset_path('map', 'map_Grass.csv'),
            'details': get_asset_path('map', 'map_Details.csv'),
            'enemies': get_asset_path('map', 'map_Enemies.csv')
        }

        graphics = {
            'floor': cut_graphics_from_sheet(get_asset_path('graphics', 'tilemap', 'Floor.png'), TILESIZE),
            'details': cut_graphics_from_sheet(get_asset_path('graphics', 'tilemap', 'details.png'), TILESIZE),
        }

        MONSTER_TYPES = list(monster_data.keys())

        for layer, path in layout_files.items():
            layout = import_csv_layout(path)
            for row_index, row in enumerate(layout):
                for col_index, cell in enumerate(row):
                    if cell != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        pos = (x, y)

                        if layer == 'floor':
                            surf = graphics['floor'][int(cell)]
                            Tile(pos, [self.visible_sprites], 'floor', surf)

                        elif layer == 'blocks':
                            Tile(pos, [self.obstacle_sprites], 'invisible')

                        elif layer == 'details':
                            surf = graphics['details'][int(cell)]
                            Tile(pos, [self.visible_sprites], 'decor', surf)

                        elif layer == 'grass':
                            grass_path = get_asset_path('graphics', 'grass', f'{cell}.png')
                            if os.path.exists(grass_path):
                                surf = pygame.image.load(grass_path).convert_alpha()
                                Tile(pos, [self.visible_sprites], 'grass', surf)

                        elif layer == 'objects':
                            try:
                                object_path = get_asset_path('graphics', 'objects', f'{cell}.png')
                                surf = pygame.image.load(object_path).convert_alpha()
                                Tile(pos, [self.visible_sprites, self.obstacle_sprites], 'object', surf)
                            except FileNotFoundError:
                                print(f"[WARNING] Object image not found: {object_path}")

                        elif layer == 'enemies':
                            try:
                                monster_type = MONSTER_TYPES[int(cell)]
                                Enemy(monster_type, pos, [self.visible_sprites, self.enemy_sprites], self.obstacle_sprites)
                            except (IndexError, ValueError):
                                print(f"[WARNING] Invalid enemy spawn index '{cell}' at position {pos}")

    def run(self):
        for sprite in self.visible_sprites:
            if hasattr(sprite, 'update'):
                if getattr(sprite, 'sprite_type', None) == 'enemy':
                    sprite.update(self.player)
                else:
                    sprite.update()

        self.visible_sprites.custom_draw()

        # # Update and draw hitsplats
        # self.player.hitsplat_group.update()
        # for sprite in self.player.hitsplat_group:
        #     if hasattr(sprite, "draw"):
        #         sprite.draw(self.display_surface)

        self.ui.display()
        self.combat_handler.update()  # Process attacks









