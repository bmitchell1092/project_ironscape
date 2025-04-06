# player.py (restored with keyboard movement and corrected path handling)
import pygame
from support import get_asset_path, import_folder
from skill import Skill, load_skills, save_skills

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # Load directional animations with correct path resolution
        self.animations = {
            'up': import_folder(get_asset_path('graphics', 'player', 'up')),
            'down': import_folder(get_asset_path('graphics', 'player', 'down')),
            'left': import_folder(get_asset_path('graphics', 'player', 'left')),
            'right': import_folder(get_asset_path('graphics', 'player', 'right'))
        }
        self.status = 'down'
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.math.Vector2()

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

        self.speed = 4 + self.skills["Agility"].level // 10
        self.update_stats()

    def update_stats(self):
        self.max_health = 10 + self.skills["Hitpoints"].level * 2
        self.health = self.max_health
        self.speed = 4 + self.skills["Agility"].level // 10
        self.damage = 1 + self.skills["Strength"].level // 10
        self.defense = self.skills["Defense"].level // 10

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0

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

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def update(self):
        self.input()
        self.move()
        self.update_stats()

        # Animate
        self.frame_index += 0.1
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def add_skill_xp(self, skill_name, xp_amount):
        if skill_name in self.skills:
            self.skills[skill_name].add_xp(xp_amount)
            self.update_stats()
            save_skills(self.skills)
        else:
            print(f"Skill '{skill_name}' does not exist!")
