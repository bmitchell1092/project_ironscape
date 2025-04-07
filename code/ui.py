import pygame
import os
from settings import *
from support import get_asset_path
from quests import QuestLog
from inventory import Inventory
from consumables import use_consumable  # Add this to use consumable logic


class UI:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 28)

        self.health_bar_rect = pygame.Rect(10, 10, 200, 20)
        self.mana_bar_rect = pygame.Rect(10, 40, 150, 15)

        self.skill_icons = {
            "Strength": pygame.image.load(get_asset_path("graphics", "icons", "strength.png")).convert_alpha(),
            "Defense": pygame.image.load(get_asset_path("graphics", "icons", "defense.png")).convert_alpha(),
            "Hitpoints": pygame.image.load(get_asset_path("graphics", "icons", "hitpoints.png")).convert_alpha(),
            "Magic": pygame.image.load(get_asset_path("graphics", "icons", "magic.png")).convert_alpha(),
            "Agility": pygame.image.load(get_asset_path("graphics", "icons", "agility.png")).convert_alpha(),
            "Herblore": pygame.image.load(get_asset_path("graphics", "icons", "herblore.png")).convert_alpha(),
            "Cooking": pygame.image.load(get_asset_path("graphics", "icons", "cooking.png")).convert_alpha()
        }

        self.item_icons = {}  # Cache for loaded item icons

        self.icon_size = 40
        self.padding_x = 20
        self.padding_y = 10
        self.columns = 3
        self.bg_color = (20, 20, 20)
        self.bg_alpha = 220
        self.hovered_skill = None

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
        self.skill_icon_rects = {}

        self.inv_columns = 5
        self.inv_rows = 5
        self.slot_size = 40
        self.slot_padding = 6
        self.inventory_slots = []
        self._generate_inventory_slots()

        self.quest_log = QuestLog("data/quests.json")
        self.inventory = Inventory("data/inventory.json")

        self.quest_scroll_offset = 0
        self.quest_scroll_speed = 20
        self.max_quest_scroll = 600
        self.quest_scrollbar_rect = pygame.Rect(WIDTH - 22, HEIGHT - 290, 12, 60)
        self.dragging_scrollbar = False
        self.quest_click_rects = []

    def _generate_inventory_slots(self):
        panel_width = 300
        margin = 10
        x = WIDTH - panel_width - margin + 20
        y = HEIGHT - 300 - margin + 60
        self.inventory_slots.clear()
        for row in range(self.inv_rows):
            for col in range(self.inv_columns):
                slot_x = x + col * (self.slot_size + self.slot_padding)
                slot_y = y + row * (self.slot_size + self.slot_padding)
                self.inventory_slots.append(pygame.Rect(slot_x, slot_y, self.slot_size, self.slot_size))

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
        ratio = 0.6
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.mana_bar_rect)
        pygame.draw.rect(self.display_surface, ENERGY_COLOR,
                         (self.mana_bar_rect.x, self.mana_bar_rect.y,
                          self.mana_bar_rect.width * ratio, self.mana_bar_rect.height))
        pygame.draw.rect(self.display_surface, TEXT_COLOR, self.mana_bar_rect, 2)

    def draw_overlay(self):
        surface = self.display_surface
        width = 300
        height = 300
        margin = 10
        x = WIDTH - width - margin
        y = HEIGHT - height - margin

        panel = pygame.Surface((width, height), pygame.SRCALPHA)
        panel.fill((*self.bg_color, self.bg_alpha))
        surface.blit(panel, (x, y))

        self.draw_tabs(x, y, width)
        pygame.draw.line(surface, (100, 100, 100), (x + 10, y + 50), (x + width - 10, y + 50), 2)

        if self.active_tab == "Skills":
            self.draw_skills_grid(x, y + 60)
        elif self.active_tab == "Inventory":
            self.draw_inventory_grid()
        elif self.active_tab == "Quests":
            self.draw_quest_log(x + 10, y + 60, width - 30, height - 70)
        else:
            self.draw_placeholder_panel(x, y + 60)

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
        self.skill_icon_rects.clear()

        for idx, (name, skill) in enumerate(skills):
            row = idx // self.columns
            col = idx % self.columns

            icon_x = x + col * (self.icon_size + self.padding_x * 2) + self.padding_x
            icon_y = y + row * (self.icon_size + self.padding_y * 2)

            icon = pygame.transform.scale(self.skill_icons[name], (self.icon_size, self.icon_size))
            icon_rect = self.display_surface.blit(icon, (icon_x, icon_y))
            self.skill_icon_rects[name] = icon_rect

            level = self.large_font.render(str(skill.level), True, (255, 255, 255))
            level_rect = level.get_rect(midleft=(icon_x + self.icon_size + 6, icon_y + self.icon_size // 2))
            self.display_surface.blit(level, level_rect)

        hover_box = pygame.Rect(x + 10, y + 180, 280, 30)
        pygame.draw.rect(self.display_surface, (30, 30, 30), hover_box, border_radius=6)
        if self.hovered_skill:
            skill = self.player.skills[self.hovered_skill]
            next_level_xp = skill.get_next_level_xp()
            exp_text = f"Exp: {skill.xp}   Exp to lvl: {next_level_xp - skill.xp}"
        else:
            exp_text = "Exp: _____   Exp to lvl: _____"
        text = self.font.render(exp_text, True, (255, 255, 255))
        self.display_surface.blit(text, (hover_box.x + 10, hover_box.y + 6))

    def draw_inventory_grid(self):
        items = self.inventory.get_items()
        for index, slot in enumerate(self.inventory_slots):
            pygame.draw.rect(self.display_surface, (100, 100, 100), slot, border_radius=4)
            pygame.draw.rect(self.display_surface, (200, 200, 200), slot, 2, border_radius=4)
            
            if index < len(items):
                item_id = items[index]["id"]
                if item_id not in self.item_icons:
                    path = get_asset_path("graphics", "items", "consumables", f"{item_id}.png")
                    self.item_icons[item_id] = pygame.image.load(path).convert_alpha()
                icon = pygame.transform.scale(self.item_icons[item_id], (self.slot_size - 4, self.slot_size - 4))
                self.display_surface.blit(icon, (slot.x + 2, slot.y + 2))


    def draw_quest_log(self, x, y, width, height):
        scroll_area = pygame.Rect(x, y, width, height)
        quest_surface = pygame.Surface((width, self.max_quest_scroll), pygame.SRCALPHA)

        self.quest_click_rects.clear()
        y_offset = 10

        weekly_quests = self.quest_log.get_weekly_quests()
        milestone_quests = self.quest_log.get_milestone_quests()

        weekly_title = self.large_font.render("Weekly", True, (255, 255, 0))
        quest_surface.blit(weekly_title, (10, y_offset))
        y_offset += 30

        for skill, quest in weekly_quests.items():
            text_color = (0, 255, 0) if quest['completed'] else (255, 0, 0)
            desc = f"{skill}: {quest['description']}"
            rendered = self.font.render(desc, True, text_color)
            rect = quest_surface.blit(rendered, (20, y_offset))
            self.quest_click_rects.append(('weekly', skill, rect))
            y_offset += 24

        y_offset += 10
        milestone_title = self.large_font.render("Milestones", True, (255, 255, 0))
        quest_surface.blit(milestone_title, (10, y_offset))
        y_offset += 30

        for skill, quests in milestone_quests.items():
            for quest in quests:
                text_color = (0, 255, 0) if quest['completed'] else (255, 0, 0)
                desc = f"{skill}: {quest['description']}"
                rendered = self.font.render(desc, True, text_color)
                rect = quest_surface.blit(rendered, (20, y_offset))
                self.quest_click_rects.append(('milestones', skill, rect))
                y_offset += 24

        scroll_view = quest_surface.subsurface(pygame.Rect(0, self.quest_scroll_offset, width, height))
        self.display_surface.blit(scroll_view, (x, y))
        pygame.draw.rect(self.display_surface, (80, 80, 80), scroll_area, 2)

        scrollbar_height = max(30, int(height * (height / self.max_quest_scroll)))
        scrollbar_y = y + int((self.quest_scroll_offset / (self.max_quest_scroll - height)) * (height - scrollbar_height))
        self.quest_scrollbar_rect = pygame.Rect(x + width + 4, scrollbar_y, 8, scrollbar_height)
        pygame.draw.rect(self.display_surface, (160, 160, 160), self.quest_scrollbar_rect)

    def draw_placeholder_panel(self, x, y):
        text = self.font.render(f"[{self.active_tab} tab coming soon]", True, (200, 200, 200))
        self.display_surface.blit(text, (x + 20, y + 20))

    def handle_mouse_click(self, mouse_pos):
        for tab, rect in self.tab_rects.items():
            if rect.collidepoint(mouse_pos):
                self.active_tab = tab
                print(f"Switched to tab: {tab}")
                return

        if self.active_tab == "Quests":
            # Scroll bar dragging logic
            if self.quest_scrollbar_rect.collidepoint(mouse_pos):
                self.dragging_scrollbar = True

            # Clickable quests
            x = WIDTH - 300 - 10 + 10  # Quest panel x
            y = HEIGHT - 300 - 10 + 60  # Quest panel y
            visible_y = y

            y_offset = 10 - self.quest_scroll_offset

            # Weekly quests
            y_offset += 30  # "Weekly" header
            for skill, quest in self.quest_log.get_weekly_quests().items():
                rect = pygame.Rect(x + 20, visible_y + y_offset, 260, 24)
                if rect.collidepoint(mouse_pos) and not quest["completed"]:
                    xp = self.quest_log.complete_weekly_quest(skill)
                    self.player.add_skill_xp(skill, xp)
                    print(f"Completed weekly quest for {skill}, +{xp} XP")
                y_offset += 24

            # Milestone quests
            y_offset += 40  # "Milestones" header
            for skill, quest_list in self.quest_log.get_milestone_quests().items():
                for quest in quest_list:
                    rect = pygame.Rect(x + 20, visible_y + y_offset, 260, 24)
                    if rect.collidepoint(mouse_pos) and not quest["completed"]:
                        xp = self.quest_log.complete_next_milestone_quest(skill)
                        self.player.add_skill_xp(skill, xp)
                        print(f"Completed milestone quest for {skill}, +{xp} XP")
                        break  # Only one milestone can be completed at a time
                    y_offset += 24
                    
        if self.active_tab == "Inventory":
            items = self.inventory.get_items()
            for index, rect in enumerate(self.inventory_slots):
                if rect.collidepoint(mouse_pos) and index < len(items):
                    item = items[index]
                    used = use_consumable(item["id"], self.player)
                    if used:
                        self.inventory.remove_item(index)
                        print(f"Used {item['id']}")

    def handle_mouse_release(self):
        self.dragging_scrollbar = False

    def handle_mouse_motion(self, mouse_pos):
        self.hovered_skill = None
        for skill, rect in self.skill_icon_rects.items():
            if rect.collidepoint(mouse_pos):
                self.hovered_skill = skill
                break
        if self.dragging_scrollbar and self.active_tab == "Quests":
            y = HEIGHT - 300 - 10 + 60
            height = 230
            rel_y = mouse_pos[1] - y
            scroll_ratio = rel_y / height
            self.quest_scroll_offset = int(scroll_ratio * (self.max_quest_scroll - height))
            self.quest_scroll_offset = max(0, min(self.quest_scroll_offset, self.max_quest_scroll - height))

    def handle_scroll(self, direction):
        if self.active_tab == "Quests":
            self.quest_scroll_offset = max(0, min(self.quest_scroll_offset + direction * self.quest_scroll_speed, self.max_quest_scroll - 230))






