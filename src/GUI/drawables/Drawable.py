from abc import ABC, abstractmethod
import pygame

class Drawable(ABC):
    @abstractmethod
    def draw(self, surface, *args, **kwargs):
        pass

    @abstractmethod
    def get_rect(self) -> pygame.Rect:
        pass