from typing import Callable

from src.GUI.draw_utils import auto_draw
from src.GUI.drawables.Drawable import Drawable
from src.GUI.drawables.ClickableMixin import ClickableMixin
from src.GUI.drawables.ResizeMixin import ResizeMixin
import pygame
class Checkbox(Drawable, ResizeMixin, ClickableMixin):

    def __init__(self, position: pygame.Rect, on_clicked: Callable, parent_surface: pygame.Surface):
        self.position = position
        self.on_clicked = on_clicked
        self.on = False
        self.__on_color = pygame.Color(0,192,0)
        self.__off_color = pygame.Color(192, 0, 0)
        super().__init__(points=['position'], surfaces=[], parent_surface=parent_surface, hitbox=self.position)

    def draw(self, surface, *args, **kwargs):
        self.resize()
        if self.on:
            auto_draw(surface, self.position, color=self.__on_color)
        else:
            auto_draw(surface, self.position, color=self.__off_color)


    def get_rect(self) -> pygame.Rect:
        return self.position

    def on_click(self):
        self.on = not self.on
        self.on_clicked()


