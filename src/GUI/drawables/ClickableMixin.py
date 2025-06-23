import pygame
from abc import ABCMeta, abstractmethod

class ClickableMixin(metaclass=ABCMeta):
    def __init__(self, hitbox: pygame.Rect, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hitbox = hitbox

    @abstractmethod
    def on_click(self):
        pass