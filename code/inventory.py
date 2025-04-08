import json
import os
from support import get_asset_path
from item import get_item_data
from consumable import use_consumable

INVENTORY_PATH = get_asset_path("data", "inventory.json")

class Inventory:
    def __init__(self, path=INVENTORY_PATH):
        self.path = path
        self.slots = [None] * 25  # row-major: left-to-right, top-to-bottom
        self.load_inventory()

    def load_inventory(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as file:
                data = json.load(file)
                items = data.get("items", [])
                for i in range(min(len(items), 25)):
                    self.slots[i] = items[i]

    def save_inventory(self):
        with open(self.path, "w") as file:
            json.dump({"items": self.slots}, file, indent=4)

    def get_items(self):
        """Return the list of item IDs in row-major order (for display)."""
        return self.slots

    def get_item_at_index(self, index):
        item_id = self.slots[index]
        return {"id": item_id} if item_id is not None else None

    def find_first_empty_slot(self):
        for index, item in enumerate(self.slots):
            if item is None:
                return index
        return -1

    def is_full(self):
        return all(slot is not None for slot in self.slots)

    def add_item(self, item_id):
        if not get_item_data(item_id):
            print(f"Item ID {item_id} not found in item registry.")
            return False

        for i in range(len(self.slots)):
            if self.slots[i] is None:
                self.slots[i] = item_id
                self.save_inventory()
                return True
        return False  # Inventory full

    def remove_item(self, index):
        if 0 <= index < len(self.slots):
            self.slots[index] = None
            self.save_inventory()

    def use_item(self, index, player):
        item_id = self.slots[index]
        item_data = get_item_data(item_id)
        if item_data and item_data["type"] == "consumable":
            used = use_consumable(item_id, player)
            if used:
                self.remove_item(index)










