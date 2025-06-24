from src.GUI.drawables.Drawable import Drawable
from src.GUI.drawables.ResizeMixin import ResizeMixin
import pygame

class ResizableTextDrawable(Drawable, ResizeMixin):
    def __init__(self, position: tuple[int, int], message: str, color: pygame.Color,
                 parent_surface: pygame.Surface, size: int = 13, bold: bool = False, centered: bool = False,
                 editable: bool = False) -> None:
        self.parent_surface = parent_surface
        self.font = pygame.font.Font('src/GUI/resources/MPLUSRounded1c-Regular.ttf' if not bold else 'src/GUI/resources/MPLUSRounded1c-ExtraBold.ttf', size=size)
        self.render = self.font.render(message, True, color)
        self.message = message
        self.color = color
        self.position = position
        self.centered = centered
        self.editable = editable
        super().__init__(points=['position'], surfaces=['render'], parent_surface=parent_surface)



    def draw(self, surface, *args, **kwargs):
        self.render = self.font.render(self.message, True, self.color)
        if self.editable: self.reinit(points=['position'], surfaces=['render'], parent_surface=self.parent_surface)
        else: self.resize()
        if not self.centered:
            surface.blit(self.render, self.position)
        else:
            new_pos = self.position[0] - self.render.get_width() / 2, self.position[1] - self.render.get_height() / 2 # - self.render.get_height() / 2
            surface.blit(self.render, new_pos)

    def get_rect(self):
        return self.render.get_rect()

