# combat.py (IRL stat-based combat system)
import pygame
from settings import weapon_data

class CombatHandler:
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies  # A sprite group of Enemy instances
        self.attack_cooldown = 500  # ms
        self.last_attack_time = 0

    def update(self):
        # Called every frame
        self.check_attacks()

    def check_attacks(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if keys[pygame.K_SPACE] and current_time - self.last_attack_time > self.attack_cooldown:
            self.last_attack_time = current_time
            self.player_attack()

    def player_attack(self):
        attack_rect = self.player.rect.inflate(40, 40)  # Expand for attack range

        for enemy in self.enemies:
            if attack_rect.colliderect(enemy.rect):
                if self.player.status.endswith('attack'):
                    if 'magic' in self.player.status:
                        base_damage = self.player.magic_damage
                    else:
                        base_damage = self.player.melee_damage

                    # Get weapon modifier
                    weapon_info = weapon_data.get(self.player.weapon, {'damage': 0})
                    weapon_bonus = weapon_info['damage']

                    # Enemy resistance
                    raw_damage = base_damage + weapon_bonus
                    final_damage = max(1, int(raw_damage / enemy.resistance**0.75))

                    enemy.take_damage(final_damage, self.player.rect.center)
                   # enemy.apply_knockback(self.player.rect.center) 
                    print(f"Player dealt {final_damage} damage to {enemy.monster_type}! Remaining HP: {enemy.health}")




