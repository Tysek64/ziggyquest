from typing import Callable

from src.GUI.draw_utils import auto_draw
from src.GUI.drawables.ClickableMixin import ClickableMixin
from src.GUI.drawables.Drawable import Drawable
from src.GUI.drawables.ResizeMixin import ResizeMixin
from src.GUI.drawables.ResizableTextDrawable import ResizableTextDrawable
import pygame

class ResizableButton(Drawable, ResizeMixin, ClickableMixin):


    def __init__(self, position: pygame.Rect, message: str,
                 background_color: pygame.Color, on_click: Callable,
                 parent_surface: pygame.Surface, font_color: pygame.Color = pygame.Color(0,0,0)):
        self.position = position
        self.message = message
        self.color = background_color
        self.on_click = on_click
        self.font_color = font_color
        self.text = ResizableTextDrawable(self.position.center, self.message, self.font_color,
                                          parent_surface, centered=True)
        super().__init__(points=['position'], surfaces=[], parent_surface=parent_surface, hitbox=self.position)

    def draw(self, surface, *args, **kwargs):
        auto_draw(surface, self.position, color=self.color)
        auto_draw(surface, self.text)



    def get_rect(self) -> pygame.Rect:
        return self.position

    def on_click(self):
        self.on_click()




