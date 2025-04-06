# support.py (now with animation loader and asset path utilities)
import pygame
import csv
import os
from settings import TILESIZE

# Reads a CSV file and returns a list of rows (used for tilemaps)
def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = csv.reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
    return terrain_map

# Slices a sprite sheet into a list of surface tiles (used for grass, objects)
def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = surface.get_width() // TILESIZE
    tile_num_y = surface.get_height() // TILESIZE

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * TILESIZE
            y = row * TILESIZE
            new_surf = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, TILESIZE, TILESIZE))
            cut_tiles.append(new_surf)

    return cut_tiles

# Utility for resolving absolute asset paths
def get_asset_path(*path_parts):
    base_path = os.path.dirname(__file__)
    return os.path.normpath(os.path.join(base_path, '..', *path_parts))

# Load all PNG images from a folder and return a list of surfaces (used for animation frames)
def import_folder(folder_path):
    full_path = get_asset_path(*folder_path)
    surface_list = []
    for filename in sorted(os.listdir(full_path)):
        if filename.endswith('.png'):
            img_path = os.path.join(full_path, filename)
            surface = pygame.image.load(img_path).convert_alpha()
            surface_list.append(surface)
    return surface_list

