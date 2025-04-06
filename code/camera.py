# camera.py
import pygame

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
        self.camera_target = None

    def set_camera_target(self, target):
        self.camera_target = target

    def custom_draw(self):
        if self.camera_target:
            self.offset.x = self.camera_target.rect.centerx - self.half_w
            self.offset.y = self.camera_target.rect.centery - self.half_h

        # 1. Draw floor tiles first
        for sprite in self.sprites():
            if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'floor':
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

        # 2. Draw everything else, sorted by centery
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if not (hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'floor'):
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)


