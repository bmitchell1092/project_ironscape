import pygame
import os
from settings import *
from tile import Tile
from player import Player
from ui import UI
from camera import YSortCameraGroup
from support import import_csv_layout, cut_graphics_from_sheet, get_asset_path

def load_individual_tiles(folder_path):
    tile_dict = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            key = int(filename.replace(".png", ""))
            tile_dict[key] = pygame.image.load(os.path.join(folder_path, filename)).convert_alpha()
    return tile_dict

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
            'grass': load_individual_tiles(get_asset_path('graphics', 'grass')),
            'objects': load_individual_tiles(get_asset_path('graphics', 'objects')),
        }

        for layer, path in layout_files.items():
            layout = import_csv_layout(path)
            for row_index, row in enumerate(layout):
                for col_index, cell in enumerate(row):
                    if cell != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        pos = (x, y)
                        idx = int(cell)

                        if layer == 'floor':
                            surf = graphics['floor'][idx]
                            Tile(pos, [self.visible_sprites], 'floor', surf)

                        elif layer == 'blocks':
                            surf = pygame.Surface((TILESIZE, TILESIZE))
                            surf.fill((0, 0, 0))
                            Tile(pos, [self.visible_sprites, self.obstacle_sprites], 'object', surf)

                        elif layer == 'objects':
                            if idx in graphics['objects']:
                                surf = graphics['objects'][idx]
                                Tile(pos, [self.visible_sprites, self.obstacle_sprites], 'object', surf)

                        elif layer == 'grass':
                            if idx in graphics['grass']:
                                surf = graphics['grass'][idx]
                                Tile(pos, [self.visible_sprites, self.obstacle_sprites], 'grass', surf)

                        elif layer == 'details':
                            surf = graphics['details'][idx]
                            Tile(pos, [self.visible_sprites], 'decor', surf)

    def run(self):
        self.visible_sprites.update()
        self.visible_sprites.custom_draw()
        self.ui.display()



