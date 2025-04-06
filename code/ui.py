import pygame
import os
from settings import *
from support import get_asset_path

class UI:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.font = pygame.font.Font(None, 24)

        self.health_bar_rect = pygame.Rect(10, 10, 200, 20)
        self.mana_bar_rect = pygame.Rect(10, 40, 150, 15)

        # Skill icons
        self.skill_icons = {
            "Strength": pygame.image.load(get_asset_path("graphics", "icons", "strength.png")).convert_alpha(),
            "Defense": pygame.image.load(get_asset_path("graphics", "icons", "defense.png")).convert_alpha(),
            "Hitpoints": pygame.image.load(get_asset_path("graphics", "icons", "hitpoints.png")).convert_alpha(),
            "Magic": pygame.image.load(get_asset_path("graphics", "icons", "magic.png")).convert_alpha(),
            "Agility": pygame.image.load(get_asset_path("graphics", "icons", "agility.png")).convert_alpha(),
            "Herblore": pygame.image.load(get_asset_path("graphics", "icons", "herblore.png")).convert_alpha(),
            "Cooking": pygame.image.load(get_asset_path("graphics", "icons", "cooking.png")).convert_alpha()
        }

        # UI layout
        self.icon_size = 32
        self.padding = 6
        self.columns = 3
        self.bg_color = (20, 20, 20)
        self.bg_alpha = 220

        # Tabs and tab state
        self.tabs = ["Skills", "Quests", "Inventory", "Equipment", "Settings"]
        self.active_tab = "Skills"
        self.tab_icons = {
            "Skills": pygame.image.load(get_asset_path("graphics", "icons", "skills_tab.png")).convert_alpha(),
            "Quests": pygame.image.load(get_asset_path("graphics", "icons", "quests_tab.png")).convert_alpha(),
            "Inventory": pygame.image.load(get_asset_path("graphics", "icons", "inventory_tab.png")).convert_alpha(),
            "Equipment": pygame.image.load(get_asset_path("graphics", "icons", "equipment_tab.png")).convert_alpha(),
            "Settings": pygame.image.load(get_asset_path("graphics", "icons", "settings_tab.png")).convert_alpha()
        }
        self.tab_rects = {}

    def display(self):
        self.draw_health_bar()
        self.draw_mana_bar()
        self.draw_overlay()

    def draw_health_bar(self):
        ratio = self.player.health / self.player.max_health
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.health_bar_rect)
        pygame.draw.rect(self.display_surface, HEALTH_COLOR,
                         (self.health_bar_rect.x, self.health_bar_rect.y,
                          self.health_bar_rect.width * ratio, self.health_bar_rect.height))
        pygame.draw.rect(self.display_surface, TEXT_COLOR, self.health_bar_rect, 2)

    def draw_mana_bar(self):
        ratio = 0.6  # Placeholder
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.mana_bar_rect)
        pygame.draw.rect(self.display_surface, MANA_COLOR,
                         (self.mana_bar_rect.x, self.mana_bar_rect.y,
                          self.mana_bar_rect.width * ratio, self.mana_bar_rect.height))
        pygame.draw.rect(self.display_surface, TEXT_COLOR, self.mana_bar_rect, 2)

    def draw_overlay(self):
        surface = self.display_surface
        width = 260
        height = 260
        margin = 10

        x = WIDTH - width - margin
        y = HEIGHT - height - margin

        panel = pygame.Surface((width, height), pygame.SRCALPHA)
        panel.fill((*self.bg_color, self.bg_alpha))
        surface.blit(panel, (x, y))

        self.draw_tabs(x, y, width)
        if self.active_tab == "Skills":
            self.draw_skills_grid(x, y + 50)
        else:
            self.draw_placeholder_panel(x, y + 50)

    def draw_tabs(self, panel_x, panel_y, panel_width):
        tab_width = 40
        tab_height = 40
        spacing = 10
        x = panel_x + (panel_width - (tab_width + spacing) * len(self.tabs)) // 2
        y = panel_y + 8

        for tab in self.tabs:
            icon = pygame.transform.scale(self.tab_icons[tab], (tab_width, tab_height))
            rect = pygame.Rect(x, y, tab_width, tab_height)
            self.display_surface.blit(icon, (x, y))
            self.tab_rects[tab] = rect

            if tab == self.active_tab:
                pygame.draw.rect(self.display_surface, (255, 255, 0), rect, 2)

            x += tab_width + spacing

    def draw_skills_grid(self, x, y):
        skills = list(self.player.skills.items())[:9]

        for idx, (name, skill) in enumerate(skills):
            row = idx // self.columns
            col = idx % self.columns

            icon_x = x + col * (self.icon_size + self.padding * 2) + self.padding + 10
            icon_y = y + row * (self.icon_size + self.padding * 2)

            icon = pygame.transform.scale(self.skill_icons[name], (self.icon_size, self.icon_size))
            self.display_surface.blit(icon, (icon_x, icon_y))

            level = self.font.render(str(skill.level), True, (255, 255, 255))
            level_rect = level.get_rect(midleft=(icon_x + self.icon_size + 4, icon_y + self.icon_size // 2))
            self.display_surface.blit(level, level_rect)

        hover_box = pygame.Rect(x + 10, y + 140, 240, 30)
        pygame.draw.rect(self.display_surface, (30, 30, 30), hover_box, border_radius=6)
        text = self.font.render("Exp: ___   Next level: ___", True, (255, 255, 255))
        self.display_surface.blit(text, (hover_box.x + 10, hover_box.y + 6))

    def draw_placeholder_panel(self, x, y):
        text = self.font.render(f"[{self.active_tab} tab coming soon]", True, (200, 200, 200))
        self.display_surface.blit(text, (x + 20, y + 20))

    def handle_mouse_click(self, mouse_pos):
        for tab, rect in self.tab_rects.items():
            if rect.collidepoint(mouse_pos):
                self.active_tab = tab
                print(f"Switched to tab: {tab}")
                break