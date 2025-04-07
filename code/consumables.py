# consumables.py
# Defines all in-game consumable items (e.g., food, potions)

CONSUMABLES = {
    "cooked_meat": {
        "name": "Cooked Meat",
        "type": "food",
        "heal_amount": 10,
        "description": "Heals 10 HP."
    },
    "mana_potion": {
        "name": "Mana Potion",
        "type": "potion",
        "mana_restore_percent": 25,
        "description": "Restores 25% of your total mana."
    }
}

def is_consumable(item_id):
    return item_id in CONSUMABLES

def get_consumable_effect(item_id):
    return CONSUMABLES.get(item_id, None)

def use_consumable(item_id, player):
    if not is_consumable(item_id):
        print(f"{item_id} is not a valid consumable.")
        return False

    effect = get_consumable_effect(item_id)
    if not effect:
        return False

    if effect["type"] == "food":
        heal_amount = effect.get("heal_amount", 0)
        if player.health < player.max_health:
            player.health = min(player.max_health, player.health + heal_amount)
            print(f"{effect['name']} used. Healed for {heal_amount} HP.")
            return True
        else:
            print("Health is already full.")
            return False

    elif effect["type"] == "potion":
        mana_percent = effect.get("mana_restore_percent", 0)
        if hasattr(player, "mana") and player.mana < player.max_mana:
            restore_amount = int(player.max_mana * (mana_percent / 100))
            player.mana = min(player.max_mana, player.mana + restore_amount)
            print(f"{effect['name']} used. Restored {restore_amount} mana.")
            return True
        else:
            print("Mana is already full or not supported.")
            return False

    return False
