from src.GUI.drawables.CompositeMixin import CompositeMixin
from src.GUI.drawables.Drawable import Drawable
import pygame
class CentrableDrawable(Drawable, CompositeMixin):
    def __init__(self, content: Drawable, parent: Drawable):
        super().__init__()
        self.parent = parent

