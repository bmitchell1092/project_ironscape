# combat.py (IRL stat-based combat system with enemy health bars)
import pygame

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
                if self.player.status == 'magic':
                    damage = 1 + self.player.skills['Magic'].level // 5
                else:
                    damage = self.player.damage  # Scaled from Strength in player.update_stats()

                enemy.take_damage(damage)
                print(f"{enemy.monster_type} took {damage} damage! Remaining HP: {enemy.health}")

                if enemy.health <= 0:
                    enemy.kill()
                    print(f"{enemy.monster_type} defeated!")

                # Show health bar
                enemy.show_health_bar = True
                enemy.health_bar_timer = pygame.time.get_ticks()


