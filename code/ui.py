import pygame
from settings import *
from support import get_asset_path
from quests import QuestLog
from inventory import *
from consumable import *
from equipment import Equipment
from item import get_item_data, get_item_image_path, get_item_type

class UI:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 28)

        self.health_bar_rect = pygame.Rect(10, 10, 200, 20)
        self.mana_bar_rect = pygame.Rect(10, 40, 150, 15)

        self.skill_icons = {
            name: pygame.image.load(get_asset_path("graphics", "icons", f"{name.lower()}.png")).convert_alpha()
            for name in ["Strength", "Defense", "Hitpoints", "Magic", "Agility", "Herblore", "Cooking"]
        }

        self.equipment_slots = {
            "Head": (0, 1),
            "Cape": (1, 0), "Neck": (1, 1), "Trinket": (1, 2),
            "Weapon": (2, 0), "Body": (2, 1), "Shield": (2, 2),
            "Legs": (3, 1),
            "Hands": (4, 0), "Feet": (4, 1), "Ring": (4, 2)
        }
        self.equipment_slot_rects = {}

        self.equipment_icons = {
            name: pygame.image.load(get_asset_path("graphics", "icons", f"{name.lower()}_slot.png")).convert_alpha()
            for name in self.equipment_slots
        }

        self.item_icons = {}

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
            name: pygame.image.load(get_asset_path("graphics", "icons", f"{name.lower()}_tab.png")).convert_alpha()
            for name in self.tabs
        }
        self.tab_rects = {}
        self.skill_icon_rects = {}

        self.inv_columns = 5
        self.inv_rows = 5
        self.slot_size = 40
        self.slot_padding = 6
        self.inventory_slots = []
        self.inventory_origin = (WIDTH - 300 - 10 + 20, HEIGHT - 300 - 10 + 60)
        self._generate_inventory_slots()

        self.quest_log = QuestLog("data/quests.json")
        self.inventory = Inventory("data/inventory.json")
        self.equipment = Equipment("data/equipment.json")

        self.quest_scroll_offset = 0
        self.quest_scroll_speed = 20
        self.max_quest_scroll = 600
        self.quest_scrollbar_rect = pygame.Rect(WIDTH - 22, HEIGHT - 290, 12, 60)
        self.dragging_scrollbar = False

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
        ratio = self.player.mana / self.player.max_mana if hasattr(self.player, 'mana') else 0.6
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
        elif self.active_tab == "Equipment":
            self.draw_equipment_tab(x + 10, y + 60)
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
            rect = self.display_surface.blit(icon, (icon_x, icon_y))
            self.skill_icon_rects[name] = rect
            level = self.large_font.render(str(skill.level), True, (255, 255, 255))
            level_rect = level.get_rect(midleft=(icon_x + self.icon_size + 6, icon_y + self.icon_size // 2))
            self.display_surface.blit(level, level_rect)

        hover_box = pygame.Rect(x + 10, y + 180, 280, 30)
        pygame.draw.rect(self.display_surface, (30, 30, 30), hover_box, border_radius=6)
        if self.hovered_skill:
            skill = self.player.skills[self.hovered_skill]
            next_level_xp = skill.get_next_level_xp()
            exp_text = f"{self.hovered_skill}: Exp {skill.xp} / {next_level_xp}"
        else:
            exp_text = "Hover over a skill to see progress"
        text = self.font.render(exp_text, True, (255, 255, 255))
        self.display_surface.blit(text, (hover_box.x + 10, hover_box.y + 6))

    def _generate_inventory_slots(self):
        panel_width = 300
        margin = 10
        x_start = WIDTH - panel_width - margin + 20
        y_start = HEIGHT - 300 - margin + 60
        self.inventory_slots.clear()
        for row in range(self.inv_rows):          # top-to-bottom
            for col in range(self.inv_columns):   # left-to-right
                slot_x = x_start + col * (self.slot_size + self.slot_padding)
                slot_y = y_start + row * (self.slot_size + self.slot_padding)
                self.inventory_slots.append(pygame.Rect(slot_x, slot_y, self.slot_size, self.slot_size))  

    def draw_inventory_grid(self):
        items = self.inventory.get_items()
        for index, rect in enumerate(self.inventory_slots):
            pygame.draw.rect(self.display_surface, (100, 100, 100), rect, border_radius=4)
            pygame.draw.rect(self.display_surface, (200, 200, 200), rect, 2, border_radius=4)

            item_id = items[index]
            if item_id is not None:
                if item_id not in self.item_icons:
                    path = get_item_image_path(item_id)
                    if os.path.exists(path):
                        self.item_icons[item_id] = pygame.image.load(path).convert_alpha()
                        print(f"Loaded {item_id} from {path}")
                    else:
                        print(f"Warning: image not found at {path}")
                        continue  # skip drawing if the image doesn't exist

                image = pygame.transform.scale(
                    self.item_icons[item_id], (self.slot_size - 4, self.slot_size - 4)
                )
                self.display_surface.blit(image, (rect.x + 2, rect.y + 2))



    def draw_quest_log(self, x, y, width, height):
        scroll_area = pygame.Rect(x, y, width, height)
        quest_surface = pygame.Surface((width, self.max_quest_scroll), pygame.SRCALPHA)
        y_offset = 10

        for section_title, quests in [
            ("Weekly", self.quest_log.get_weekly_quests()),
            ("Milestones", self.quest_log.get_milestone_quests())
        ]:
            quest_surface.blit(self.large_font.render(section_title, True, (255, 255, 0)), (10, y_offset))
            y_offset += 30
            for skill, qlist in (quests.items() if section_title == "Milestones" else [(k, [v]) for k, v in quests.items()]):
                for quest in qlist:
                    desc = f"{skill}: {quest['description']}"
                    color = (0, 255, 0) if quest['completed'] else (255, 0, 0)
                    quest_surface.blit(self.font.render(desc, True, color), (20, y_offset))
                    y_offset += 24
            y_offset += 10

        scroll_view = quest_surface.subsurface(pygame.Rect(0, self.quest_scroll_offset, width, height))
        self.display_surface.blit(scroll_view, (x, y))
        pygame.draw.rect(self.display_surface, (80, 80, 80), scroll_area, 2)

        bar_height = max(30, int(height * (height / self.max_quest_scroll)))
        bar_y = y + int((self.quest_scroll_offset / (self.max_quest_scroll - height)) * (height - bar_height))
        self.quest_scrollbar_rect = pygame.Rect(x + width + 4, bar_y, 8, bar_height)
        pygame.draw.rect(self.display_surface, (160, 160, 160), self.quest_scrollbar_rect)

    def draw_equipment_tab(self, x, y):
        start_x = x + 10
        start_y = y
        spacing = 10
        slot_size = 40

        # Draw equipment slot icons
        self.equipment_slot_rects = {}
        for name, (row, col) in self.equipment_slots.items():
            slot_x = start_x + col * (slot_size + spacing)
            slot_y = start_y + row * (slot_size + spacing)
            self.equipment_slot_rects[name] = pygame.Rect(slot_x, slot_y, slot_size, slot_size)

            icon = pygame.transform.scale(self.equipment_icons[name], (slot_size, slot_size))
            self.display_surface.blit(icon, (slot_x, slot_y))

            # Draw equipped item if present
            item_id = self.equipment.get_equipped_items(name)
            if item_id:
                if item_id not in self.item_icons:
                    path = get_item_image_path(item_id)
                    if os.path.exists(path):
                        self.item_icons[item_id] = pygame.image.load(path).convert_alpha()
                if item_id in self.item_icons:
                    image = pygame.transform.scale(self.item_icons[item_id], (slot_size - 4, slot_size - 4))
                    self.display_surface.blit(image, (slot_x + 2, slot_y + 2))

        # ---- Draw stat bonuses ----
        total_str, total_def, total_mag, total_acc = self.get_total_equipment_bonuses()

        stat_x = start_x + 3 * (slot_size + spacing) + 20
        stat_y = start_y

        headers = [("Attack", total_acc), ("Defense", total_def), ("Magic", total_mag)]
        for header, value in headers:
            header_text = self.large_font.render(header, True, (255, 255, 0))
            bonus_text = self.font.render(f"+{value}", True, (200, 200, 200))
            self.display_surface.blit(header_text, (stat_x, stat_y))
            self.display_surface.blit(bonus_text, (stat_x, stat_y + 28))
            stat_y += 70

        # Strength bonus at the bottom
        str_text = self.font.render(f"Strength Bonus: +{total_str}", True, (255, 255, 0))
        self.display_surface.blit(str_text, (stat_x, stat_y + 10))


        # Draw placeholder bonuses
        bonus_x = start_x + 3 * (slot_size + spacing) + 10
        bonus_y = start_y + 10
        bonuses = ["Str bonus", "Def bonus", "Mag Dmg"]
        for bonus in bonuses:
            text = self.font.render(bonus, True, (255, 255, 0))
            self.display_surface.blit(text, (bonus_x, bonus_y))
            bonus_y += 40

    def get_total_equipment_bonuses(self):
        total_acc = 0
        total_str = 0
        total_def = 0
        total_mag = 0

        for slot, item_id in self.equipment.slots.items():
            if item_id is not None:
                item = get_item_data(item_id)
                if item:
                    total_acc += item.get("accuracy", 0)
                    total_str += item.get("strength", 0)
                    total_def += item.get("defense", 0)
                    total_mag += item.get("magic", 0)

        return total_acc, total_str, total_def, total_mag        

    def draw_placeholder_panel(self, x, y):
        msg = f"[{self.active_tab} tab coming soon]"
        self.display_surface.blit(self.font.render(msg, True, (200, 200, 200)), (x + 20, y + 20))

    def handle_mouse_click(self, mouse_pos):
        # Check if any tab is clicked
        for tab, rect in self.tab_rects.items():
            if rect.collidepoint(mouse_pos):
                self.active_tab = tab
                return

        # Inventory item click handling
        if self.active_tab == "Inventory":
            for i, rect in enumerate(self.inventory_slots):
                if rect.collidepoint(mouse_pos):
                    item = self.inventory.get_item_at_index(i)
                    if item is not None:
                        item_data = get_item_data(item["id"])
                        if item_data["type"] in ["weapon", "armor"]:
                            slot = item_data["slot"]
                            if slot:
                                existing = self.equipment.get_equipped_items(slot)
                                if existing:
                                    self.inventory.add_item(existing)
                                self.equipment.equip_item(slot, item["id"])
                                self.inventory.remove_item(i)
                        else:
                            self.inventory.use_item(i, self.player)
                    return

        # Quest log click handling
        if self.active_tab == "Quests":
            if self.quest_scrollbar_rect.collidepoint(mouse_pos):
                self.dragging_scrollbar = True

            x = WIDTH - 300 - 10 + 10
            y = HEIGHT - 300 - 10 + 60
            visible_y = y
            y_offset = 10 - self.quest_scroll_offset
            y_offset += 30
            for skill, quest in self.quest_log.get_weekly_quests().items():
                rect = pygame.Rect(x + 20, visible_y + y_offset, 260, 24)
                if rect.collidepoint(mouse_pos) and not quest["completed"]:
                    xp = self.quest_log.complete_weekly_quest(skill)
                    self.player.add_skill_xp(skill, xp)
                y_offset += 24
            y_offset += 40
            for skill, quests in self.quest_log.get_milestone_quests().items():
                for quest in quests:
                    rect = pygame.Rect(x + 20, visible_y + y_offset, 260, 24)
                    if rect.collidepoint(mouse_pos) and not quest["completed"]:
                        xp = self.quest_log.complete_next_milestone_quest(skill)
                        self.player.add_skill_xp(skill, xp)
                        break
                    y_offset += 24

        if self.active_tab == "Equipment":
            for slot, rect in self.equipment_slot_rects.items():
                if rect.collidepoint(mouse_pos):
                    item_id = self.equipment.get_equipped_items(slot)
                    if item_id:
                        if self.inventory.add_item(item_id):
                            self.equipment.unequip_item(slot)
                    return


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
            ratio = rel_y / height
            self.quest_scroll_offset = int(ratio * (self.max_quest_scroll - height))
            self.quest_scroll_offset = max(0, min(self.quest_scroll_offset, self.max_quest_scroll - height))

    def handle_scroll(self, direction):
        if self.active_tab == "Quests":
            self.quest_scroll_offset = max(0, min(self.quest_scroll_offset + direction * self.quest_scroll_speed, self.max_quest_scroll - 230))







