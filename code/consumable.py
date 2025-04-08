# consumable.py
from item import get_item_data


"""Defines effects for consumable items (food, potions, etc.)."""

def use_consumable(item_id, player):
    data = get_item_data(item_id)
    if not data or data["type"] != "consumable":
        return False

    subtype = data.get("subtype")

    if subtype == "food":
        heal = data.get("heal_amount", 0)
        player.health = min(player.max_health, player.health + heal)
        return True

    elif subtype == "potion":
        restore_pct = data.get("mana_restore_percent", 0)
        if hasattr(player, "mana") and hasattr(player, "max_mana"):
            restore_amount = int(player.max_mana * restore_pct)
            player.mana = min(player.max_mana, player.mana + restore_amount)
            return True

    return False

def apply_consumable_effect(player, item_data):
    """Apply the effect of a consumable item to the player."""
    subtype = item_data.get("subtype")
    if subtype == "food":
        # Heal the player by a fixed amount, without exceeding max health
        heal_amount = item_data.get("heal_amount", 0)
        if hasattr(player, "health") and hasattr(player, "max_health"):
            player.health = min(player.health + heal_amount, player.max_health)
            # Optionally, you could print or log the heal
            # e.g., print(f"{player} healed for {heal_amount} HP")
    elif subtype == "potion":
        # Restore a percentage of the player's mana (or energy)
        restore_pct = item_data.get("mana_restore_percent", 0)
        # If mana is tracked as 'mana' on player:
        if hasattr(player, "mana") and hasattr(player, "max_mana"):
            amount = int(player.max_mana * restore_pct)
            player.mana = min(player.mana + amount, player.max_mana)
        # If the game uses 'energy' for mana, use player.energy and player.stats['energy'] or similar:
        elif hasattr(player, "energy") and hasattr(player, "max_energy"):
            amount = int(player.max_energy * restore_pct)
            player.energy = min(player.energy + amount, player.max_energy)
    else:
        # Unknown consumable subtype; no effect.
        print(f"Consumable effect for subtype '{subtype}' is not implemented.")

