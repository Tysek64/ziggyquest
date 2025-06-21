import pygame
from src.GUI.draw_utils import auto_draw

class SurfaceRenderer:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.render_objects = [] # list of pairs (drawable, draw_info). Draw info includes color etc.

    def register(self, object):
        self.render_objects.append(object)

    def draw(self):
        for drawable, draw_info in self.render_objects:
            auto_draw(self.surface, drawable, **draw_info)

    def update(self):
        pygame.display.update(self.surface.get_rect()) # updatuje tylko zmieniona czesc





