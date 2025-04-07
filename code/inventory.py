# inventory.py (updated to support 25-slot layout and item rendering)
import json
import os
import pygame
from support import get_asset_path
from consumables import CONSUMABLES

INVENTORY_PATH = get_asset_path("data", "inventory.json")

class Inventory:
    def __init__(self, path=INVENTORY_PATH):
        self.path = path
        self.slots = [None] * 25  # Fixed size inventory
        self.load_inventory()

    def load_inventory(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as file:
                data = json.load(file)
                items = data.get("items", [])
                for idx, item in enumerate(items):
                    if idx < 25:
                        self.slots[idx] = item

    def save_inventory(self):
        with open(self.path, "w") as file:
            json.dump({"items": self.slots}, file, indent=4)

    def add_item(self, item_name):
        for idx in range(len(self.slots)):
            if self.slots[idx] is None:
                self.slots[idx] = item_name
                self.save_inventory()
                return True
        return False  # Inventory full

    def use_item(self, index, player):
        item_name = self.slots[index]
        if item_name and item_name in CONSUMABLES:
            effect = CONSUMABLES[item_name]
            if effect.get("heal"):
                player.health = min(player.max_health, player.health + effect["heal"])
            if effect.get("mana_restore"):
                # Placeholder: apply mana restoration logic when mana system is added
                pass
            self.slots[index] = None
            self.save_inventory()

    def get_item_image(self, item_name):
        if item_name and item_name in CONSUMABLES:
            image_path = CONSUMABLES[item_name].get("image")
            if image_path:
                return pygame.image.load(image_path).convert_alpha()
        return None



