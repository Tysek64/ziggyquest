from typing import Callable

from src.GUI.draw_utils import auto_draw
from src.GUI.drawables.CompositeMixin import CompositeMixin
from src.GUI.drawables.EditableTextField import EditableTextField
from src.GUI.drawables.ResizeMixin import ResizeMixin
from src.GUI.drawables.ResizableButton import ResizableButton
from src.GUI.drawables.ResizableTextDrawable import ResizableTextDrawable
import pygame

class ResizableInputPopup(ResizeMixin, CompositeMixin):
    def __init__(self, position: pygame.Rect, text: str, color: pygame.Color,
                 on_cancel: Callable,
                 on_accept: Callable,
                 parent_surface: pygame.Surface,
                 text_color: pygame.Color = pygame.Color(0, 0, 0), default_value: str = ''):
        self.position = position
        self.on_cancel = on_cancel
        self.on_accept = on_accept
        self.color = color
        self.__top_margin = 5
        self.__left_margin = 20
        self.__font_size = self.position.height // 5
        self.__button_size = (self.position.width / 3, self.position.height / 6) # wybrane dowolnie, zeby ladnie wygladalo
        self.__text_field_size = (self.position.width - 2 * self.__left_margin, self.position.height / 3)

        text_pos = (self.position.left + self.__left_margin, self.position.top + self.__top_margin)
        self.text = ResizableTextDrawable(text_pos, text, text_color, parent_surface, size=self.__font_size // 2)

        # Start stacking from below the text
        input_y = text_pos[1] + self.text.render.get_height() + self.__top_margin
        input_pos = (self.position.left + self.__left_margin, input_y)
        self.input = EditableTextField(pygame.Rect(input_pos, self.__text_field_size), parent_surface,
                                       font_size=self.__font_size)

        # Below input
        button_y = input_pos[1] + self.__text_field_size[1] + self.__top_margin
        cancel_pos = (self.position.left + self.__left_margin, button_y)
        self.cancel_button = ResizableButton(pygame.Rect(cancel_pos, self.__button_size), 'Cancel',
                                             pygame.Color(255, 128, 0), on_cancel, parent_surface)

        accept_pos = (self.position.right - self.__left_margin - self.__button_size[0], button_y)
        self.accept_button = ResizableButton(pygame.Rect(accept_pos, self.__button_size), 'Confirm',
                                             pygame.Color(128, 255, 0), on_accept, parent_surface)


        self._rendered_objects = [self.input, self.accept_button, self.cancel_button]
        self.points = [self.input.position.topleft, self.accept_button.position.topleft, self.cancel_button.position.topleft]

        super().__init__(points=['position'], surfaces=[], parent_surface=parent_surface)

        self.current_value = default_value

    def draw(self, surface, *args, **kwargs):
        self.resize()
        auto_draw(surface, self.position, color=self.color)
        auto_draw(surface, self.text)
        auto_draw(surface, self.input)
        auto_draw(surface, self.cancel_button)
        auto_draw(surface, self.accept_button)

    def get_rect(self) -> pygame.Rect:
        return self.position