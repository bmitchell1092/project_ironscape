# equipment.py
import json
import os
from support import get_asset_path
from item import get_item_data

EQUIPMENT_PATH = get_asset_path("data", "equipment.json")

SLOT_ORDER = [
    "Head", "Cape", "Neck",
    "Weapon", "Body", "Shield",
    "Legs", "Hands", "Feet", "Ring"
]

class Equipment:
    def __init__(self, path=EQUIPMENT_PATH):
        self.path = path
        self.slots = {slot: None for slot in SLOT_ORDER}
        self.load_equipment()

    def load_equipment(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as file:
                data = json.load(file)
                for slot in SLOT_ORDER:
                    self.slots[slot] = data.get(slot, None)

    def save_equipment(self):
        with open(self.path, "w") as file:
            json.dump(self.slots, file, indent=4)

    def get_equipped_items(self, slot):
        return self.slots.get(slot)

    def equip_item(self, slot, item_id):
        if slot in SLOT_ORDER and get_item_data(item_id):
            self.slots[slot] = item_id
            self.save_equipment()

    def unequip_item(self, slot):
        if slot in SLOT_ORDER:
            self.slots[slot] = None
            self.save_equipment()
