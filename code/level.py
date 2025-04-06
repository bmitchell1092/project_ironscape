# level.py (fixed tile layering + all tile types restored)
import pygame
import os
from settings import *
from tile import Tile
from player import Player
from enemy import Enemy
from support import import_csv_layout, get_asset_path
from ui import UI

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.ui = None
        self.player = None

        self.create_map()

    def load_tiles_from_folder(self, folder_name):
        folder_path = get_asset_path('graphics', folder_name)
        tiles = []
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith('.png'):
                path = os.path.join(folder_path, filename)
                tiles.append(pygame.image.load(path).convert_alpha())
        return tiles

    def create_map(self):
        layouts = {
            'floor': import_csv_layout(get_asset_path('map', 'map_Floor.csv')),
            'boundary': import_csv_layout(get_asset_path('map', 'map_FloorBlocks.csv')),
            'grass': import_csv_layout(get_asset_path('map', 'map_Grass.csv')),
            'object': import_csv_layout(get_asset_path('map', 'map_Objects.csv')),
        }

        floor_tiles = self.load_tiles_from_folder('tilemap')
        grass_tiles = self.load_tiles_from_folder('grass')
        object_tiles = self.load_tiles_from_folder('objects')

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, cell in enumerate(row):
                    if cell != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        tile_index = int(cell)

                        if style == 'floor':
                            if 0 <= tile_index < len(floor_tiles):
                                tile_surf = floor_tiles[tile_index]
                                Tile((x, y), [self.visible_sprites], 'floor', tile_surf)

                        elif style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')

                        elif style == 'grass':
                            if 0 <= tile_index < len(grass_tiles):
                                tile_surf = grass_tiles[tile_index]
                                Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'grass', tile_surf)

                        elif style == 'object':
                            if 0 <= tile_index < len(object_tiles):
                                tile_surf = object_tiles[tile_index]
                                Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', tile_surf)

        self.player = Player((100, 100))
        self.visible_sprites.add(self.player)
        self.ui = UI(self.player)

    def run(self):
        self.display_surface.fill((50, 50, 50))
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

