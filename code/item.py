# item.py
from support import get_asset_path
"""Central item registry: defines item attributes and provides lookup functions."""

ITEM_DATA = {
    # Weapon example
    1001: {
        "id": 1001,
        "name": "Iron Sword",
        "type": "weapon",
        "subtype": None,
        "description": "A sturdy iron sword.",
        "damage": 10,
        "cooldown": 500,
    },
    # Armor example
    2001: {
        "id": 2001,
        "name": "Bronze Platelegs",
        "type": "armor",
        "subtype": "legs",
        "description": "Basic bronze plateleg armor.",
        "defense": 5,
    },
    2002: {
        "id": 2002,
        "name": "Bronze Medium Helm",
        "type": "armor",
        "subtype": "head",
        "description": "Basic bronze helmet",
        "defense": 3,
    },
    2003: {
        "id": 2003,
        "name": "Bronze Platebody",
        "type": "armor",
        "subtype": "body",
        "description": "Basic bronze platebody armor.",
        "defense": 6,
    },
    # Consumable - Food example
    3001: {
        "id": 3001,
        "name": "Bread",
        "type": "consumable",
        "subtype": "food",
        "description": "Simple food that restores a small amount of health.",
        "heal_amount": 5
    },
    # Consumable - Potion example
    3003: {
        "id": 2003,
        "name": "Mana Potion",
        "type": "consumable",
        "subtype": "potion",
        "description": "Magical potion that restores 50% of max mana.",
        "mana_restore_percent": 0.5
    },
    # Add more items here...
}

def get_item_data(item_id):
    """Retrieve the metadata dictionary for the given item_id."""
    return ITEM_DATA.get(item_id)


def get_item_image_path(item_id):
    data = get_item_data(item_id)
    if not data:
        return None

    item_type = data["type"]
    filename = f"{item_id}.png"  # Ensure your image files are named like 2002.png
    return get_asset_path("graphics", "items", item_type, filename)


def get_item_type(item_id):
    """Returns the type of the item (e.g., 'weapon', 'consumable', etc.)"""
    data = get_item_data(item_id)
    return data["type"] if data else None



