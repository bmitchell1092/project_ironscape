# main.py (updated to handle UI tab switching)
import pygame
from level import Level
from settings import WIDTH, HEIGHT, FPS

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Project Ironscape")
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                # Handle mouse clicks for UI tab switching
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    self.level.ui.handle_mouse_click(mouse_pos)

                # Handle mouse motion for UI skill hover
                if event.type == pygame.MOUSEMOTION:
                    self.level.ui.handle_mouse_motion(event.pos)

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.level.ui.handle_mouse_release()

                if event.type == pygame.MOUSEWHEEL:
                        self.level.ui.handle_scroll(-event.y)
   

            #self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
