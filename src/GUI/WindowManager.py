import pygame
from src.GUI.SurfaceRenderer import SurfaceRenderer
from src.GUI.ObjectLoader import ObjectLoader
from time import sleep
import sys

class WindowManager:
    def __init__(self, pygame_lock, window_width: int = 640, window_height: int = 400) -> None:
        self.size = self.width, self_height = window_width, window_height
        self.display = None
        self.renderers = None
        self._running = False
        self.pygame_lock = pygame_lock

    def setup_game(self) -> None:
        pygame.init()
        pygame.display.set_mode(self.size, pygame.HWSURFACE
                                | pygame.DOUBLEBUF)
        self._running = True

    # renderers must be created after setup_game
    def hook_renderers(self, renderers: list[SurfaceRenderer]):
        self.renderers = renderers

    def run_game(self) -> None:
        if not self._running:
            raise ValueError('Game was not set up (call setup_game)')

        with self.pygame_lock:
            while self._running:
                sleep(0.05)
                for event in pygame.event.get():
                    self.process_event(event)

                pygame.display.get_surface().fill(pygame.Color(255, 255, 255))
                for renderer in self.renderers:
                    renderer.draw()

                pygame.display.update()

            pygame.quit()

    def process_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self._running = False

    def close(self):
        self._running = False

if __name__ == '__main__':
    game = WindowManager()
    game.setup_game()
    renderers = [
        SurfaceRenderer(pygame.display.get_surface())
    ]

    render_objects = ObjectLoader().load()
    for renderer in renderers:
        for render_object in render_objects:
            renderer.register(render_object)

    game.hook_renderers(renderers)
    game.run_game()


