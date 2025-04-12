# player.py
import os
import pygame
from support import get_asset_path, import_folder
from skill import Skill, load_skills, save_skills
from melee import Weapon
from magic import MagicManager
from equipment import Equipment

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, obstacle_sprites, sprite_group, groups):
        super().__init__(sprite_group)
        self.sprite_group = sprite_group

        # Load animations
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

        self.groups = groups  # i.e., the main visible_sprites group
        self.status = 'down'
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.z_index = 2

        self.direction = pygame.math.Vector2()
        self.obstacle_sprites = obstacle_sprites

        # Equipment
        self.equipment = Equipment("data/equipment.json")

        # Combat
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.weapon = None

        # Load skills
        self.skills = load_skills()
        if not self.skills:
            self.skills = {
                "Strength": Skill("Strength"),
                "Hitpoints": Skill("Hitpoints"),
                "Cooking": Skill("Cooking"),
                "Defense": Skill("Defense"),
                "Agility": Skill("Agility"),
                "Smithing": Skill("Smithing"),
                "Magic": Skill("Magic"),
                "Herblore": Skill("Herblore"),
                "Farming": Skill("Farming"),
            }
        self.set_stats_from_skills()

        # Initialize the MagicManager
        self.magic_manager = MagicManager()
        # NEW: load magic frames now that display is set up
        self.magic_manager.load_assets()

    def set_stats_from_skills(self):
        self.max_health = self.skills["Hitpoints"].level
        self.health = self.max_health
        self.max_mana = 10 + self.skills["Magic"].level * 5
        self.mana = self.max_mana
        self.speed = 4 + self.skills["Agility"].level // 10
        self.melee_damage = 1 + self.skills["Strength"].level // 3
        self.magic_damage = 1 + self.skills["Magic"].level // 3
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

            # Melee attack
            if keys[pygame.K_SPACE]:
                self.attack()
                print("Space key pressed, attacking!")

            # Magic casting
            if keys[pygame.K_q]:
                self.magic_manager.cast(self, self.groups, 'Q')
            if keys[pygame.K_e]:
                self.magic_manager.cast(self, self.groups, 'E')
            if keys[pygame.K_LCTRL]:
                self.magic_manager.cast(self, self.groups, 'LCTRL')

    def attack(self):
        self.attacking = True
        self.attack_time = pygame.time.get_ticks()
        self.direction.x = 0
        self.direction.y = 0
        self.status = self.status.split('_')[0] + '_attack'
        self.frame_index = 0

        weapon_id = self.equipment.get_equipped_items("Weapon")
        if weapon_id:
            self.weapon = Weapon(self, self.sprite_group)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking and current_time - self.attack_time >= self.attack_cooldown:
            self.attacking = False

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

    def add_skill_xp(self, skill_name, xp_amount):
        if skill_name in self.skills:
            self.skills[skill_name].add_xp(xp_amount)
            self.set_stats_from_skills()
            save_skills(self.skills)
        else:
            print(f"Skill '{skill_name}' does not exist!")









