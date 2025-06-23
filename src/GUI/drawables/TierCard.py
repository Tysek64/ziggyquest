from src.GUI.drawables.Drawable import Drawable
from src.GUI.drawables.ResizableTextDrawable import ResizableTextDrawable
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

        self.__margin = 20
        self.image = None if character.loaded_image is None else pygame.image.load(io.BytesIO(character.loaded_image))
        if self.image is not None: self.image = pygame.transform.scale(self.image, (rect.w - 2 * self.__margin,
                                                                                    rect.h/3 - self.__margin))
        pic_coords = (rect.topleft[0] + self.__margin, rect.topleft[1] + self.__margin)
        text_coords = (rect.topleft[0] + self.__margin + int(self.image.get_width() / 2),
                       rect.topleft[1] + self.__margin + self.image.get_height())

        self.pic = ResizableImageDrawable(parent_surface, self.image, pic_coords)
        self.text = ResizableTextDrawable(text_coords, 'Łamacz kawy', pygame.Color('ivory3'),
                                          parent_surface, size=30, centered=True)
        super().__init__(hitbox=rect, points=['rect'], surfaces=[], parent_surface=parent_surface)

    def draw(self, surface, *args, **kwargs):
        self.resize()
        auto_draw(surface, self.rect, color=self.color)
        if self.image is not None: auto_draw(surface, self.pic)
        auto_draw(surface, self.text)

    def on_click(self):
        pass

