import pygame
import sys
from CodeFolder.config import BASE_WIDTH, BASE_HEIGHT, FPS, BG_COLOR
from CodeFolder.scenes.menu import MainMenu

class Game:
    def __init__(self):
        pygame.init()
        # НАСТРОЙКА ПОЛНОЭКРАННОГО РЕЖИМА
        self.screen = pygame.display.set_mode(
            (BASE_WIDTH, BASE_HEIGHT), 
            pygame.SCALED | pygame.FULLSCREEN
        )
        pygame.display.set_caption("Ashfall")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Запускаем главное меню
        self.current_scene = MainMenu(self)

    def change_scene(self, new_scene):
        self.current_scene = new_scene

    def quit_game(self):
        self.running = False

    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.1)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.current_scene.handle_event(event)

            self.current_scene.update(dt)

            self.screen.fill(BG_COLOR)
            self.current_scene.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()