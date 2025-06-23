from src.GUI.drawables.Drawable import Drawable
from src.GUI.drawables.ResizeMixin import ResizeMixin
from src.GUI.drawables.ClickableMixin import ClickableMixin
from src.GUI.drawables.ResizableImageDrawable import ResizableImageDrawable
from src.GUI.draw_utils import auto_draw
from src.backend.character import Character
import pygame
import io

class TierCard(ClickableMixin, ResizeMixin, Drawable):
    def __init__(self, character: Character, rect: pygame.Rect,
                 color: pygame.Color, parent_surface: pygame.Surface):
        self.rect = rect
        self.character = character
        self.color = color
        self.image = None if character.loaded_image is None else pygame.image.load(io.BytesIO(character.loaded_image))
        self.pic = ResizableImageDrawable(parent_surface, self.image, rect.midtop)
        super().__init__(hitbox=rect, points=['rect'], surfaces=[], parent_surface=parent_surface)

    def draw(self, surface, *args, **kwargs):
        self.resize()
        auto_draw(surface, self.rect, color=self.color)
        if self.image is not None: auto_draw(surface, self.pic)

    def on_click(self):
        pass

