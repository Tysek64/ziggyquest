from abc import ABCMeta, ABC

from src.GUI.drawables.Drawable import Drawable


class CompositeMixin(Drawable, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert hasattr(self, '_rendered_objects') # inner elements
        assert hasattr(self, 'points') # position of inner elements