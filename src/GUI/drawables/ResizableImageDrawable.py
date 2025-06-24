from src.GUI.drawables.ImageDrawable import ImageDrawable
from src.GUI.drawables.ResizeMixin import ResizeMixin
import pygame
from pathlib import Path

class ResizableImageDrawable(ImageDrawable, ResizeMixin):
    def __init__(self,
                 parent_surface: pygame.Surface,
                 image: Path | pygame.Surface,
                 position: tuple[int, int] | pygame.Rect,
                 size: tuple[int, int] | None = None,
                 crop: pygame.Rect | None = None):
        ImageDrawable.__init__(self, image, position, size, crop)
        ResizeMixin.__init__(self, points=['position'], surfaces=['image_surface'], parent_surface=parent_surface)

    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        self.resize()
        super().draw(surface, *args, **kwargs)

