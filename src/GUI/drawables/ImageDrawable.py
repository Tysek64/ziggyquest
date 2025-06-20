import pygame

from src.GUI.drawables.Drawable import Drawable
from pathlib import Path
# position is a tuple of upper left corner (x,y)
# size is tuple width, height
# size is predefined size (width, height)
class ImageDrawable(Drawable):
    def __init__(self, image: Path | pygame.Surface,
                 position: tuple[int, int] | pygame.Rect,
                 size: tuple[int, int] | None = None,
                 crop: pygame.Rect | None = None):

        self.position = position
        self.image_surface = pygame.image.load(image) if isinstance(image, Path) else image
        if size is not None:
            self.image_surface = pygame.transform.scale(self.image_surface, size)

        self.crop = crop


    def draw(self, surface: pygame.Surface, *args, **kwargs) -> None:
        surface.blit(self.image_surface, self.position, self.crop)
