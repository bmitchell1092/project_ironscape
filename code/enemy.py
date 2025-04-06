# enemy.py (updated with dynamic enemy sprite loading and safe pathing)
import pygame
from settings import *
from support import get_asset_path

class Enemy(pygame.sprite.Sprite):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles):
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # Load enemy image based on monster name
        filename = f"{monster_name}.png"
        try:
            image_path = get_asset_path('graphics', 'enemies', filename)
            self.image = pygame.image.load(image_path).convert_alpha()
        except FileNotFoundError:
            self.image = pygame.Surface((TILESIZE, TILESIZE))
            self.image.fill('red')

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)

        # Enemy attributes
        self.health = 30
        self.exp = 100
        self.speed = 2
        self.attack_damage = 10
        self.resistance = 3
        self.attack_radius = 50
        self.notice_radius = 200
        self.attack_type = 'slash'

        # Interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles

        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

        # Sounds
        self.death_sound = pygame.mixer.Sound(get_asset_path('audio', 'death.wav'))
        self.hit_sound = pygame.mixer.Sound(get_asset_path('audio', 'hit.wav'))
        self.attack_sound = pygame.mixer.Sound(get_asset_path('audio', 'attack.wav'))
        self.death_sound.set_volume(0.6)
        self.hit_sound.set_volume(0.6)
        self.attack_sound.set_volume(0.6)

        self.obstacle_sprites = obstacle_sprites

    def get_damage(self, player):
        return max(0, self.attack_damage - player.defense)

    def attack(self, player):
        if self.can_attack:
            self.attack_sound.play()
            self.can_attack = False
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)

    def receive_damage(self, player):
        if self.vulnerable:
            self.hit_sound.play()
            damage = max(0, player.damage - self.resistance)
            self.health -= damage
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.trigger_death_particles(self.rect.center, self.sprite_type)
            self.death_sound.play()
            self.kill()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack and current_time - self.attack_time >= self.attack_cooldown:
            self.can_attack = True
        if not self.vulnerable and current_time - self.hit_time >= self.invincibility_duration:
            self.vulnerable = True

    def update(self):
        self.cooldowns()
        self.check_death()
