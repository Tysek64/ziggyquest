from src.GUI.drawables.ClickableMixin import ClickableMixin
from abc import abstractmethod, ABC
import pygame
class FocusableMixin(ClickableMixin, ABC):
    def __init__(self, hitbox: pygame.Rect, has_focus: bool = False, *args, **kwargs):
        super().__init__(hitbox, *args, **kwargs)
        self.has_focus = has_focus

    def on_click(self):
        self.has_focus = True

    @abstractmethod
    def on_input(self, input_key):
        pass