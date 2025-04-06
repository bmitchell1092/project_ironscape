# level.py (with camera group, z-ordering, and player visibility)
import pygame
from settings import *
from tile import Tile
from player import Player
from ui import UI
from support import import_csv_layout, cut_graphics_from_sheet, get_asset_path

# Camera group to handle rendering and scrolling
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

        # Create camera box centered on screen
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

    def custom_draw(self, player):
        # Update offset based on player position
        self.offset.x = player.rect.centerx - self.half_w
        self.offset.y = player.rect.centery - self.half_h

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # Sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # Load player
        self.player = Player((100, 100))
        self.visible_sprites.add(self.player)
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

                        if layer == 'floor':
                            surf = graphics['floor'][int(cell)]
                            Tile((x, y), [self.visible_sprites], 'floor', surf)

                        elif layer == 'blocks':
                            surf = pygame.Surface((TILESIZE, TILESIZE))
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)

                        elif layer == 'objects':
                            surf = graphics['objects'][int(cell)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)

                        elif layer == 'grass':
                            surf = graphics['grass'][int(cell)]
                            Tile((x, y), [self.visible_sprites], 'grass', surf)

                        elif layer == 'details':
                            surf = graphics['details'][int(cell)]
                            Tile((x, y), [self.visible_sprites], 'decor', surf)

    def run(self):
        self.visible_sprites.update()
        self.visible_sprites.custom_draw(self.player)
        self.ui.display()
