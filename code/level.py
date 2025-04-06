# level.py (finalized with correct rendering order and collision)
import pygame
from settings import *
from tile import Tile
from player import Player
from ui import UI
from camera import YSortCameraGroup
from support import import_csv_layout, cut_graphics_from_sheet, get_asset_path
import os

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # Sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # Load player
        self.player = Player((1000, 1000), self.obstacle_sprites)
        self.visible_sprites.add(self.player)
        self.visible_sprites.set_camera_target(self.player)
        self.ui = UI(self.player)

        # Map loading
        self.create_map()

    def create_map(self):
        layout_files = {
            'floor': get_asset_path('map', 'map_Floor.csv'),
            'blocks': get_asset_path('map', 'map_FloorBlocks.csv'),
            'objects': get_asset_path('map', 'map_Objects.csv'),
            'grass': get_asset_path('map', 'map_Grass.csv'),
            'details': get_asset_path('map', 'map_Details.csv'),
        }

        graphics = {
            'floor': cut_graphics_from_sheet(get_asset_path('graphics', 'tilemap', 'Floor.png'), TILESIZE),
            'details': cut_graphics_from_sheet(get_asset_path('graphics', 'tilemap', 'details.png'), TILESIZE),
        }

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
                            # Create invisible colliders only
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


    def run(self):
        self.visible_sprites.update()
        self.visible_sprites.custom_draw()
        self.ui.display()




