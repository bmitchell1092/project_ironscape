# enemy.py
import pygame
from support import import_folder

monster_data = {
    'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'audio/attack/slash.wav', 'speed': 3, 'resistance': 2, 'attack_radius': 50, 'notice_radius': 300},
    'chibi': {'health': 100,'exp':3000,'damage':1,'attack_type': 'leaf_attack', 'attack_sound':'audio/attack/slash.wav', 'speed': 4, 'resistance': 2, 'attack_radius': 50, 'notice_radius': 300},
    'raccoon': {'health': 100,'exp':250,'damage':5,'attack_type': 'claw',  'attack_sound':'audio/attack/claw.wav','speed': 1, 'resistance': 4, 'attack_radius': 120, 'notice_radius': 400},
    'spirit': {'health': 50,'exp':110,'damage':1,'attack_type': 'thunder', 'attack_sound':'audio/attack/fireball.wav', 'speed': 4, 'resistance': 1, 'attack_radius': 60, 'notice_radius': 350},
    'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360}
}

class Enemy(pygame.sprite.Sprite):
    def __init__(self, monster_type, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.monster_type = monster_type
        self.obstacle_sprites = obstacle_sprites
        self.z_index = 4

        # Load animations
        self.animations = {'idle': [], 'move': [], 'attack': []}
        for animation in self.animations.keys():
            full_path = f'graphics/monsters/{monster_type}/{animation}'
            self.animations[animation] = import_folder(full_path)

        self.frame_index = 0
        self.status = 'idle'
        self.animation_speed = 0.15
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)

        # Stats from monster_data
        monster_info = monster_data[monster_type]
        self.health = monster_info['health']
        self.max_health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.resistance = monster_info['resistance']
        self.attack_damage = monster_info['damage']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']

        # Timers
        self.can_attack = True
        self.attack_cooldown = 800
        self.attack_time = None

        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

        # Knockback
        self.knockback_velocity = pygame.math.Vector2()
        self.knockback_duration = 100  # milliseconds
        self.knockback_timer = 0

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        direction = (player_vec - enemy_vec).normalize() if distance > 0 else pygame.math.Vector2()
        return distance, direction

    def take_damage(self, amount, source_position=None):
        if self.vulnerable:
            self.health -= amount
            self.vulnerable = False
            self.hit_time = pygame.time.get_ticks()
            print(f"{self.monster_type} took {amount} damage! Remaining HP: {self.health}")

            if source_position:
                self.apply_knockback(source_position)

    def check_death(self):
        if self.health <= 0:
            self.kill()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.vulnerable and current_time - self.hit_time >= self.invincibility_duration:
            self.vulnerable = True
        if not self.can_attack and current_time - self.attack_time >= self.attack_cooldown:
            self.can_attack = True

    def apply_knockback(self, source_position):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        source_vec = pygame.math.Vector2(source_position)

        try:
            knockback_direction = (enemy_vec - source_vec).normalize()
            knockback_distance = 50  # tweakable
            knockback_vector = knockback_direction * knockback_distance
            self.rect.center += knockback_vector
        except ValueError:
            print(f"[WARNING] Knockback skipped for {self.monster_type} due to zero-length vector.")

    def move(self, player):
        distance, direction = self.get_player_distance_direction(player)

        if distance <= self.attack_radius and self.can_attack:
            self.attack(player)
        elif distance <= self.notice_radius:
            self.status = 'move'
            buffer_zone = 10
            if distance > self.attack_radius - buffer_zone:
                self.rect.center += direction * self.speed
        else:
            self.status = 'idle'

    def attack(self, player):
        print(f"{self.monster_type} attacks!")
        self.status = 'attack'
        if self.can_attack:
            self.can_attack = False
            self.attack_time = pygame.time.get_ticks()
            raw_damage = self.attack_damage
            mitigation = player.defense
            mitigated = max(1, raw_damage - mitigation)
            player.health -= mitigated
            print(f"{self.monster_type} dealt {mitigated} damage. Player HP: {player.health}")

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]

    def draw_health_bar(self, offset):
        if self.health < self.max_health:
            display_surface = pygame.display.get_surface()
            bar_width = self.rect.width
            bar_height = 5
            health_ratio = self.health / self.max_health

            screen_x = self.rect.left - offset.x
            screen_y = self.rect.top - offset.y - 10

            bg_rect = pygame.Rect(screen_x, screen_y, bar_width, bar_height)
            fg_rect = pygame.Rect(screen_x, screen_y, bar_width * health_ratio, bar_height)

            pygame.draw.rect(display_surface, 'red', bg_rect)
            pygame.draw.rect(display_surface, 'green', fg_rect)

    def update(self, player):
        self.cooldowns()
        self.move(player)
        self.animate()
        self.check_death()





