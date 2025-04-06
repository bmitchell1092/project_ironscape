import pygame
from settings import *
from tile import Tile
from player import Player
from ui import UI
from support import import_csv_layout, cut_graphics_from_sheet, get_asset_path

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
        self.camera_target = None

    def set_camera_target(self, target):
        self.camera_target = target

    def custom_draw(self):
        if self.camera_target:
            self.offset.x = self.camera_target.rect.centerx - self.half_w
            self.offset.y = self.camera_target.rect.centery - self.half_h

        for sprite in sorted(self.sprites(), key=lambda spr: (getattr(spr, 'z_index', 2), spr.rect.centery)):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.player = Player((1000, 1000))
        self.visible_sprites.add(self.player)
        self.visible_sprites.set_camera_target(self.player)
        self.ui = UI(self.player)

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
                            surf.fill((0, 0, 0))
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
        self.visible_sprites.custom_draw()
        self.ui.display()


