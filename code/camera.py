# camera.py
import pygame

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.camera_target = None

    def set_camera_target(self, target):
        self.camera_target = target

    def custom_draw(self):
        if self.camera_target:
            self.offset.x = self.camera_target.rect.centerx - self.half_w
            self.offset.y = self.camera_target.rect.centery - self.half_h

        # Draw all sprites using z_index first, then y-position
        sorted_sprites = sorted(
            self.sprites(),
            key=lambda s: (getattr(s, 'z_index', 0), s.rect.centery)
        )

        # Store enemies needing health bars
        enemies_with_health_bars = []

        for sprite in sorted_sprites:
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

            # Check if sprite is a damaged enemy
            if hasattr(sprite, 'health') and hasattr(sprite, 'max_health') and sprite.health < sprite.max_health:
                enemies_with_health_bars.append((sprite, offset_pos))

        # Draw health bars on top of all other sprites
        for sprite, offset_pos in enemies_with_health_bars:
            self.draw_health_bar(sprite, offset_pos)

    def draw_health_bar(self, sprite, offset_pos):
        health_bar_width = 40
        health_bar_height = 6
        bar_offset_y = -12  # slightly above the sprite

        health_ratio = sprite.health / sprite.max_health
        bg_rect = pygame.Rect(offset_pos[0], offset_pos[1] + bar_offset_y, health_bar_width, health_bar_height)
        fg_rect = pygame.Rect(offset_pos[0], offset_pos[1] + bar_offset_y, health_bar_width * health_ratio, health_bar_height)

        pygame.draw.rect(self.display_surface, 'red', bg_rect)
        pygame.draw.rect(self.display_surface, 'green', fg_rect)
        pygame.draw.rect(self.display_surface, 'black', bg_rect, 1)




