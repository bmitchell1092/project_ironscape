# level.py (cleaned and corrected rendering logic)
import pygame
from settings import *
from tile import Tile
from player import Player
from ui import UI
from camera import YSortCameraGroup
from support import import_csv_layout, cut_graphics_from_sheet, get_asset_path

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # Sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # Load player
        self.player = Player((1000, 1000))  # Adjust spawn as needed
        self.visible_sprites.add(self.player)
        self.visible_sprites.set_camera_target(self.player)

        # UI
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
            'objects': cut_graphics_from_sheet(get_asset_path('graphics', 'tilemap', 'ground.png'), TILESIZE),
            'grass': cut_graphics_from_sheet(get_asset_path('graphics', 'tilemap', 'ground.png'), TILESIZE),
            'details': cut_graphics_from_sheet(get_asset_path('graphics', 'tilemap', 'details.png'), TILESIZE),
        }

        for layer, path in layout_files.items():
            layout = import_csv_layout(path)
            for row_index, row in enumerate(layout):
                for col_index, cell in enumerate(row):
                    if cell != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        position = (x, y)

                        if layer == 'floor':
                            surf = graphics['floor'][int(cell)]
                            Tile(position, [self.visible_sprites], 'floor', surf)

                        elif layer == 'blocks':
                            surf = pygame.Surface((TILESIZE, TILESIZE))
                            surf.fill((0, 0, 0))  # temporary black tile
                            Tile(position, [self.visible_sprites, self.obstacle_sprites], 'object', surf)

                        elif layer == 'objects':
                            surf = graphics['objects'][int(cell)]
                            Tile(position, [self.visible_sprites, self.obstacle_sprites], 'object', surf)

                        elif layer == 'grass':
                            surf = graphics['grass'][int(cell)]
                            Tile(position, [self.visible_sprites], 'grass', surf)

                        elif layer == 'details':
                            surf = graphics['details'][int(cell)]
                            Tile(position, [self.visible_sprites], 'decor', surf)

    def run(self):
        self.visible_sprites.update()
        self.visible_sprites.custom_draw()
        self.ui.display()
