from src.GUI.drawables.Drawable import Drawable
from src.GUI.drawables.ResizeMixin import ResizeMixin
import pygame

class ResizableTextDrawable(Drawable, ResizeMixin):
    def __init__(self, position: tuple[int, int], message: str, color: pygame.Color,
                 parent_surface: pygame.Surface, size: int = 13, bold: bool = False) -> None:
        self.font = pygame.font.SysFont('monospace', bold=bold, size=size)
        self.render = self.render = self.font.render(message, True, color)
        self.message = message
        self.color = color
        self.position = position
        super().__init__(points=['position'], surfaces=['render'], parent_surface=parent_surface)

    def draw(self, surface, *args, **kwargs):
        self.render = self.font.render(self.message, True, self.color)
        self.resize()
        surface.blit(self.render, self.position)

