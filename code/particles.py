# particles.py (flame damage now animation-bound)
import pygame
from support import import_folder
from random import randint

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups, damage=0, targets=None):
        super().__init__(groups)
        self.frames = animation_frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z_index = 4
        self.damage = damage
        self.targets = targets or []
        self.hit_enemies = set()

    def update(self):
        self.frame_index += 0.2
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

        # Apply damage only once during the animation
        if self.damage and self.targets:
            for enemy in self.targets:
                if self.rect.colliderect(enemy.rect) and enemy not in self.hit_enemies:
                    enemy.take_damage(self.damage, self.rect.center)
                    self.hit_enemies.add(enemy)

class AnimationPlayer:
    def __init__(self):
        self.frames = {
            'flame': import_folder('graphics/particles/flame/frames'),
            'aura': import_folder('graphics/particles/aura'),
            'heal': import_folder('graphics/particles/heal')
        }

    def create_particles(self, animation_type, pos, groups, damage=0, targets=None):
        animation_frames = self.frames.get(animation_type)
        if animation_frames:
            ParticleEffect(pos, animation_frames, groups, damage, targets)