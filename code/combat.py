# combat.py (updated)
import pygame
from item import get_item_data
from melee import Weapon

class CombatHandler:
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies
        self.attack_cooldown = 500  # ms
        self.last_attack_time = 0

    def update(self):
        self.check_melee_attacks()
        self.check_magic_attacks()

    def check_melee_attacks(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if keys[pygame.K_SPACE] and current_time - self.last_attack_time > self.attack_cooldown:
            self.last_attack_time = current_time
            self.perform_melee_attack()

    def perform_melee_attack(self):
        weapon_id = self.player.equipment.get_equipped_items("Weapon")
        weapon_data = get_item_data(weapon_id) if weapon_id else {}
        weapon_range = weapon_data.get("range", 40)
        weapon_damage = weapon_data.get("damage", 0)

        # Bonus from all equipped gear
        equipment_bonus = self.player.equipment.get_total_bonus("melee")

        attack_rect = self.player.rect.inflate(weapon_range, weapon_range)

        for enemy in self.enemies:
            if attack_rect.colliderect(enemy.rect) and self.player.status.endswith('attack'):
                base_damage = self.player.melee_damage
                total_damage = base_damage + weapon_damage + equipment_bonus
                final_damage = max(1, int(total_damage / enemy.resistance**0.75))

                enemy.take_damage(final_damage, self.player.rect.center)
                print(f"[Melee] {enemy.monster_type} took {final_damage} damage.")

    def check_magic_attacks(self):
        spell_name = self.player.magic_manager.get_selected_spell('damage')
        spell = self.player.magic_manager.magic_data.get(spell_name)

        if not spell:
            return

        spell_damage = spell.get("potency", 0)
        equipment_bonus = self.player.equipment.get_total_bonus("magic")

        direction = self.get_direction_vector(self.player.status)
        for i in range(1, 6):
            offset = direction * i * 64  # TILESIZE
            flame_pos = pygame.Vector2(self.player.rect.center) + offset
            flame_hitbox = pygame.Rect(flame_pos.x - 12, flame_pos.y - 12, 24, 24)

            for enemy in self.enemies:
                if flame_hitbox.colliderect(enemy.rect):
                    base_damage = self.player.magic_damage
                    total_damage = base_damage + equipment_bonus + spell_damage
                    final_damage = max(1, int(total_damage / enemy.resistance**0.75))

                    enemy.take_damage(final_damage, flame_pos)
                    print(f"[Magic] {enemy.monster_type} took {final_damage} damage from {spell_name}.")

    def get_direction_vector(self, status):
        direction = status.split('_')[0]
        return {
            'right': pygame.Vector2(1, 0),
            'left': pygame.Vector2(-1, 0),
            'up': pygame.Vector2(0, -1),
            'down': pygame.Vector2(0, 1)
        }.get(direction, pygame.Vector2(0, 0))


