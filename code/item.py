# item.py
from support import get_asset_path

item_data = {
    "meat": {
        "name": "Meat",
        "type": "food",
        "heal": 10,
        "image": get_asset_path("graphics", "items", "meat.png")
    },
    "iron_sword": {
        "name": "Iron Sword",
        "type": "weapon",
        "damage": 5,
        "image": get_asset_path("graphics", "items", "iron_sword.png")
    },
    "iron_axe": {
        "name": "Iron Axe",
        "type": "weapon",
        "damage": 5,
        "image": get_asset_path("graphics", "items", "iron_axe.png")
    },
    "health_potion": {
        "name": "Health Potion",
        "type": "potion",
        "heal": 20,
        "image": get_asset_path("graphics", "items", "health_potion.png")
    },
    "bronze_helmet": {
        "name": "Bronze Helmet",
        "type": "armor",
        "slot": "head",
        "defense": 2,
        "image": get_asset_path("graphics", "items", "bronze_helmet.png")
    }
}
