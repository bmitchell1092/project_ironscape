# enemy.py (IRL stat-based enemies with health bar rendering)
import pygame
from settings import monster_data
from support import import_folder

class Enemy(pygame.sprite.Sprite):
    def __init__(self, monster_type, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        self.monster_type = monster_type
        self.obstacle_sprites = obstacle_sprites

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

        # Stats from settings
        monster_info = monster_data[monster_type]
        self.health = monster_info['health']
        self.max_health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
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

        self.display_health_bar = False
        self.health_bar_duration = 1500  # ms
        self.health_bar_timer = 0

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        direction = (player_vec - enemy_vec).normalize() if distance > 0 else pygame.math.Vector2()
        return distance, direction

    def take_damage(self, amount):
        if self.vulnerable:
            self.health -= amount
            self.vulnerable = False
            self.hit_time = pygame.time.get_ticks()
            self.display_health_bar = True
            self.health_bar_timer = pygame.time.get_ticks()
            print(f"{self.monster_type} took {amount} damage! Remaining HP: {self.health}")

    def check_death(self):
        if self.health <= 0:
            self.kill()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.vulnerable and current_time - self.hit_time >= self.invincibility_duration:
            self.vulnerable = True
        if not self.can_attack and current_time - self.attack_time >= self.attack_cooldown:
            self.can_attack = True
        if self.display_health_bar and current_time - self.health_bar_timer >= self.health_bar_duration:
            self.display_health_bar = False

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]

    def move(self, player):
        distance, direction = self.get_player_distance_direction(player)
        if distance <= self.attack_radius and self.can_attack:
            self.attack(player)
        elif distance <= self.notice_radius:
            self.status = 'move'
            self.rect.center += direction * self.speed
        else:
            self.status = 'idle'

    def attack(self, player):
        self.status = 'attack'
        self.attack_time = pygame.time.get_ticks()
        self.can_attack = False

        # Calculate mitigated damage
        mitigated = max(0, self.attack_damage - player.defense)
        player.health -= mitigated
        print(f"{self.monster_type} attacks! {self.monster_type} dealt {mitigated} damage. Player HP: {player.health}")

    def draw_health_bar(self, surface):
        if self.display_health_bar:
            ratio = self.health / self.max_health
            bar_width = 40
            bar_height = 6
            bar_x = self.rect.centerx - bar_width // 2
            bar_y = self.rect.top - 12

            bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
            fg_rect = pygame.Rect(bar_x, bar_y, int(bar_width * ratio), bar_height)

            pygame.draw.rect(surface, 'red', bg_rect)
            pygame.draw.rect(surface, 'green', fg_rect)

    def update(self, player):
        self.cooldowns()
        self.move(player)
        self.animate()
        self.check_death()
        self.draw_health_bar(pygame.display.get_surface())



