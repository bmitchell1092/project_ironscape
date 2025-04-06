# support.py (updated to include import_folder)
import pygame
import csv
import os

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = csv.reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
    return terrain_map

def cut_graphics_from_sheet(sheet_path, tile_size):
    sheet = pygame.image.load(sheet_path).convert_alpha()
    sheet_width, sheet_height = sheet.get_size()
    tile_list = []

    for row in range(sheet_height // tile_size):
        for col in range(sheet_width // tile_size):
            x, y = col * tile_size, row * tile_size
            new_surf = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
            new_surf.blit(sheet, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            tile_list.append(new_surf)

    return tile_list

def import_folder(folder_path):
    surface_list = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.png'):
            full_path = os.path.join(folder_path, filename)
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list

def get_asset_path(*path_parts):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    return os.path.join(base_dir, *path_parts)

def draw_text(surface, text, font, color, pos):
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, pos)
