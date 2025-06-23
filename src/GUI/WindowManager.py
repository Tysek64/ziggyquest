import urllib.request
from pathlib import Path
from time import sleep

import pygame
from src.GUI.SurfaceRenderer import SurfaceRenderer
from src.GUI.ObjectLoader import ObjectLoader
import threading
from threading import Lock
import sys

from src.GUI.drawables.ClickableMixin import ClickableMixin
from src.GUI.drawables.CompositeMixin import CompositeMixin
from src.GUI.drawables.VerticalDrawable import VerticalDrawable
from src.backend.character.CharacterParser import CharacterFactory


class WindowManager:
    def __init__(self, pygame_lock: threading.Lock, window_width: int = 1280, window_height: int = 720) -> None:
        self.size = self.width, self_height = window_width, window_height
        self.display = None
        self.renderers = None
        self._running = False
        self.pygame_lock = pygame_lock

    # renderers must be created after setup_game
    def hook_renderers(self, renderers: list[SurfaceRenderer]):
        self.renderers = renderers

    def setup(self):
        self.pygame_lock.acquire()
        pygame.init()
        pygame.display.set_mode(self.size, pygame.HWSURFACE
                                | pygame.DOUBLEBUF | pygame.RESIZABLE)
        self._running = True

    def run(self) -> None:
        while self._running:
            sleep(0.05)
            for event in pygame.event.get():
                self.process_event(event)

            pygame.display.get_surface().fill(pygame.Color(255, 255, 255))
            for renderer in self.renderers:
                renderer.draw()

            pygame.display.update()

        pygame.quit()
        self.pygame_lock.release()


    def process_event(self, event: pygame.event.Event) -> None:
        match event.type:
            case pygame.QUIT:
                self._running = False
            case pygame.MOUSEBUTTONDOWN:
                for renderer in self.renderers:
                    for object_ in renderer.render_objects:
                        obj = object_[0]
                        if isinstance(obj, ClickableMixin) and obj.hitbox.collidepoint(pygame.mouse.get_pos()):
                            object_.on_click()

                        if isinstance(obj, CompositeMixin) and obj.get_rect().collidepoint(pygame.mouse.get_pos()):
                            for element, pos in zip(obj._rendered_objects, obj.points):
                                if isinstance(element, ClickableMixin):
                                    new_hitbox = pygame.Rect(pos, element.hitbox.size)
                                    if new_hitbox.collidepoint(pygame.mouse.get_pos()):
                                        element.on_click()




    def close(self):
        self._running = False

if __name__ == '__main__':
    from threading import Lock
    game = WindowManager(Lock())
    game.setup()
    renderers = [
        SurfaceRenderer(pygame.display.get_surface())
    ]

    ch0 = CharacterFactory().make_characters(Path('./characters'))[0]

    url = 'https://kwojt.kieg.science/user/images/g5_helium/testimonials/KW_opt.jpg'
    print(f'Fetching profile pic from {url}...')
    request = urllib.request.urlopen(url)
    ch0.loaded_image = request.read()
    render_objects = ObjectLoader().load(pygame.display.get_surface(), ch0)
    for renderer in renderers:
        for render_object in render_objects:
            renderer.register(render_object)

    game.hook_renderers(renderers)
    game.run()


