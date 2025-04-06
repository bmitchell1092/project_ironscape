# player.py (finalized with idle, movement, and weapon attack animation)
import os
import pygame
from support import get_asset_path, import_folder
from skill import Skill, load_skills, save_skills
from weapon import Weapon  # Make sure this import is present

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, obstacle_sprites, sprite_group):
        super().__init__(sprite_group)
        self.sprite_group = sprite_group
        self.obstacle_sprites = obstacle_sprites

        # Load all animations
        self.animations = {
            'up': import_folder(get_asset_path('graphics', 'player', 'up')),
            'down': import_folder(get_asset_path('graphics', 'player', 'down')),
            'left': import_folder(get_asset_path('graphics', 'player', 'left')),
            'right': import_folder(get_asset_path('graphics', 'player', 'right')),

            'up_idle': import_folder(get_asset_path('graphics', 'player', 'up_idle')),
            'down_idle': import_folder(get_asset_path('graphics', 'player', 'down_idle')),
            'left_idle': import_folder(get_asset_path('graphics', 'player', 'left_idle')),
            'right_idle': import_folder(get_asset_path('graphics', 'player', 'right_idle')),

            'up_attack': import_folder(get_asset_path('graphics', 'player', 'up_attack')),
            'down_attack': import_folder(get_asset_path('graphics', 'player', 'down_attack')),
            'left_attack': import_folder(get_asset_path('graphics', 'player', 'left_attack')),
            'right_attack': import_folder(get_asset_path('graphics', 'player', 'right_attack')),
        }

        self.status = 'down'
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # Movement
        self.direction = pygame.math.Vector2()
        self.speed = 4
        self.weapon = None

        # Combat
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        # Load or initialize skills
        self.skills = load_skills()
        if not self.skills:
            self.skills = {
                "Strength": Skill("Strength"),
                "Defense": Skill("Defense"),
                "Hitpoints": Skill("Hitpoints"),
                "Magic": Skill("Magic"),
                "Agility": Skill("Agility"),
                "Herblore": Skill("Herblore"),
                "Cooking": Skill("Cooking"),
            }

        self.update_stats()

    def update_stats(self):
        self.max_health = self.skills["Hitpoints"].level
        self.health = self.max_health
        self.speed = 4 + self.skills["Agility"].level // 10
        self.damage = 1 + self.skills["Strength"].level // 10
        self.defense = self.skills["Defense"].level // 10

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0

        if not self.attacking:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'

            if keys[pygame.K_SPACE]:
                self.attack()

    def attack(self):
        self.attacking = True
        self.attack_time = pygame.time.get_ticks()
        self.direction.x = 0
        self.direction.y = 0
        self.status = self.status.split('_')[0] + '_attack'
        self.frame_index = 0

        # Spawn weapon sprite
        self.weapon = Weapon(self, self.sprite_group)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking and current_time - self.attack_time >= self.attack_cooldown:
            self.attacking = False
            if self.weapon:
                self.weapon.kill()
                self.weapon = None

    def get_status(self):
        if self.attacking:
            self.status = self.status.split('_')[0] + '_attack'
        elif self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * self.speed
        self.collision('horizontal')

        self.rect.y += self.direction.y * self.speed
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.rect.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.rect.left = sprite.hitbox.right
                elif direction == 'vertical':
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:
                        self.rect.top = sprite.hitbox.bottom

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += 0.15
        if self.frame_index >= len(animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False
                if self.weapon:
                    self.weapon.kill()
                    self.weapon = None
        self.image = animation[int(self.frame_index)]

    def update(self):
        self.input()
        self.cooldowns()
        self.move()
        self.get_status()
        self.animate()
        self.update_stats()

    def add_skill_xp(self, skill_name, xp_amount):
        if skill_name in self.skills:
            self.skills[skill_name].add_xp(xp_amount)
            self.update_stats()
            save_skills(self.skills)
        else:
            print(f"Skill '{skill_name}' does not exist!")





