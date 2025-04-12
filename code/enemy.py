# enemy.py
import pygame
import os
from support import import_folder

monster_data = {
    'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'audio/attack/slash.wav', 'speed': 3, 'resistance': 2, 'attack_radius': 50, 'attack_range': 50, 'is_ranged': False, 'notice_radius': 300, 'attack_cooldown': 2000, 'attack_duration': 500},
    'chibi': {'health': 100,'exp':3000,'damage':1,'attack_type': 'leaf_attack', 'attack_sound':'audio/attack/slash.wav', 'speed': 4, 'resistance': 2, 'attack_radius': 50, 'attack_range': 50, 'is_ranged': False, 'notice_radius': 300, 'attack_cooldown': 2000, 'attack_duration': 500},
    'raccoon': {'health': 100,'exp':250,'damage':5,'attack_type': 'claw', 'attack_sound':'audio/attack/claw.wav','speed': 1, 'resistance': 4, 'attack_radius': 120, 'attack_range': 120, 'is_ranged': False, 'notice_radius': 400, 'attack_cooldown': 1800, 'attack_duration': 500},
    'spirit': {'health': 50,'exp':110,'damage':1,'attack_type': 'thunder', 'attack_sound':'audio/attack/fireball.wav', 'speed': 4, 'resistance': 1, 'attack_radius': 60, 'attack_range': 200, 'is_ranged': True, 'notice_radius': 350, 'attack_cooldown': 1500, 'attack_duration': 400},
    'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'attack_range': 80, 'is_ranged': False, 'notice_radius': 360, 'attack_cooldown': 2500, 'attack_duration': 600}
}

class Enemy(pygame.sprite.Sprite):
    def __init__(self, monster_type, pos, groups, obstacle_sprites):
        self.patrol_vector = pygame.Vector2()
        self.patrol_timer = 0
        self.patrol_interval = 2000
        self.returning_home = False
        self.return_threshold = 8
        super().__init__(groups)
        self.spawn_point = pygame.Vector2(pos)
        self.patrol_radius = 100
        self.sprite_type = 'enemy'
        self.monster_type = monster_type
        self.obstacle_sprites = obstacle_sprites
        self.z_index = 4

        # Load animations
        self.animations = {'idle': [], 'move': [], 'attack': [], 'death': []}
        for animation in self.animations.keys():
            full_path = f'graphics/monsters/{monster_type}/{animation}'
            self.animations[animation] = import_folder(full_path)

        self.frame_index = 0
        self.status = 'idle'
        self.animation_speed = 0.10
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
        self.attack_cooldown = monster_info['attack_cooldown']
        self.attack_duration = monster_info['attack_duration']
        self.attack_range = monster_info.get('attack_range', self.attack_radius)
        self.is_ranged = monster_info.get('is_ranged', False)

        # Load attack sound
        sound_path = monster_info['attack_sound']
        if os.path.exists(sound_path):
            self.attack_sound = pygame.mixer.Sound(sound_path)
            self.attack_sound.set_volume(0.2)
        else:
            print(f"[WARNING] Attack sound not found for {self.monster_type}: {sound_path}")
            self.attack_sound = None

        # Timers
        self.can_attack = True
        self.attack_time = None
        self.attack_anim_time = 0

        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

        self.alive = True

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
            if source_position is not None:
                self.apply_knockback(source_position)
            

    def check_death(self):
        if self.health <= 0 and self.alive:
            self.alive = False
            self.frame_index = 0
            self.status = 'death'

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.vulnerable and current_time - self.hit_time >= self.invincibility_duration:
            self.vulnerable = True
        if not self.can_attack and current_time - self.attack_time >= self.attack_cooldown:
            self.can_attack = True

    def apply_knockback(self, source_position):
        enemy_vec = pygame.math.Vector2(self.hitbox.center)
        source_vec = pygame.math.Vector2(source_position)
        try:
            knockback_direction = (enemy_vec - source_vec).normalize()
            knockback_distance = 50  # adjust if needed
            knockback_vector = knockback_direction * knockback_distance

            self.hitbox.center += knockback_vector
            self.rect.center = self.hitbox.center  # sync visible sprite to new hitbox
        except ValueError:
            print(f"[WARNING] Knockback skipped for {self.monster_type} due to zero-length vector.")

    def move(self, player):
        if self.status == 'return' and self.returning_home:
            self.status = 'move'
            direction = (self.spawn_point - pygame.Vector2(self.hitbox.center)).normalize()
            distance = pygame.Vector2(self.hitbox.center).distance_to(self.spawn_point)
            if distance > self.return_threshold:
                self.hitbox.centerx += direction.x * self.speed
                self.collision('horizontal')
                self.hitbox.centery += direction.y * self.speed
                self.collision('vertical')
                self.rect.center = self.hitbox.center
            else:
                self.returning_home = False
                self.status = 'idle'
                self.patrol_timer = 0
            return
        current_time = pygame.time.get_ticks()
        if self.status == 'idle':
            if current_time - self.patrol_timer > self.patrol_interval:
                from random import choice
                self.patrol_vector = pygame.Vector2(choice([-1, 0, 1]), choice([-1, 0, 1]))
                self.patrol_vector = self.patrol_vector.normalize() if self.patrol_vector.length() != 0 else pygame.Vector2()
                self.patrol_timer = current_time

            if self.patrol_vector.length() > 0:
                self.status = 'move'
            else:
                if self.status != 'return':
                    self.status = 'return'
                    self.returning_home = True

            future_pos = pygame.Vector2(self.hitbox.center) + self.patrol_vector * self.speed * 0.5
            if future_pos.distance_to(self.spawn_point) <= self.patrol_radius:
                self.hitbox.centerx += self.patrol_vector.x * self.speed * 0.5
                self.collision('horizontal')
                self.hitbox.centery += self.patrol_vector.y * self.speed * 0.5
                self.collision('vertical')
                self.rect.center = self.hitbox.center
            else:
                self.patrol_vector = pygame.Vector2()
                self.patrol_timer = 0
            self.collision('horizontal')
            self.hitbox.centery += self.patrol_vector.y * self.speed * 0.5
            self.collision('vertical')
            self.rect.center = self.hitbox.center
        if not self.alive:
            return

        current_time = pygame.time.get_ticks()
        if self.status == 'attack' and current_time - self.attack_anim_time < self.attack_duration:
            return

        distance, direction = self.get_player_distance_direction(player)
        if distance <= self.attack_radius and self.can_attack:
            self.attack(player)

        elif distance <= self.notice_radius:
            self.status = 'move'
            if not self.is_ranged or distance > self.attack_range:
                self.hitbox.centerx += direction.x * self.speed
                self.collision('horizontal')
                self.hitbox.centery += direction.y * self.speed
                self.collision('vertical')
                self.rect.center = self.hitbox.center
        else:
            self.status = 'idle'

    def collision(self, direction):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.hitbox.centerx > sprite.hitbox.centerx:
                        self.hitbox.left = sprite.hitbox.right
                    else:
                        self.hitbox.right = sprite.hitbox.left
                if direction == 'vertical':
                    if self.hitbox.centery > sprite.hitbox.centery:
                        self.hitbox.top = sprite.hitbox.bottom
                    else:
                        self.hitbox.bottom = sprite.hitbox.top

    def attack(self, player):
        if not self.can_attack or not self.alive:
            return
        print(f"{self.monster_type} attacks!")
        self.status = 'attack'
        now = pygame.time.get_ticks()
        self.attack_time = now
        self.attack_anim_time = now
        self.can_attack = False

        if self.attack_sound:
            self.attack_sound.play()

        raw_damage = self.attack_damage
        mitigation = player.defense
        mitigated = max(1, raw_damage - mitigation)
        player.health -= mitigated
        print(f"{self.monster_type} dealt {mitigated} damage. Player HP: {player.health}")

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'death':
                self.kill()
                return
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




















