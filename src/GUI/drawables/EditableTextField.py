from src.GUI.draw_utils import auto_draw
from src.GUI.drawables.Drawable import Drawable
from src.GUI.drawables.ResizableTextDrawable import ResizableTextDrawable
from src.GUI.drawables.ResizeMixin import ResizeMixin
from src.GUI.drawables.FocusableMixin import FocusableMixin
import pygame

class EditableTextField(Drawable, ResizeMixin, FocusableMixin):
    def __init__(self, position: pygame.Rect, parent_surface: pygame.Surface,
                 color: pygame.Color = pygame.Color(48, 48, 48),
                 default_value: str = 'abacada', max_len=16):
        self.position = position
        self.color = color
        self.rendered_text = ResizableTextDrawable(self.position.topleft, default_value,
                                                   pygame.Color(0, 255, 0), parent_surface, editable=True)
        self.max_len = max_len
        super().__init__(points=['position'], surfaces=[], parent_surface=parent_surface, hitbox=self.position)

    def draw(self, surface, *args, **kwargs):
        self.resize()
        self.rendered_text.resize()
        auto_draw(surface, self.position, color=self.color)
        auto_draw(surface, self.rendered_text)

    def get_rect(self) -> pygame.Rect:
        return self.position

    def on_input(self, input_key):
        print(ord('0'), ord('9'), ord('.'), input_key)
        if (ord('0') <= input_key <= ord('9') or input_key == ord('.')) and len(self.rendered_text.message) < self.max_len:
            self.rendered_text.message = self.rendered_text.message + chr(input_key)
        elif input_key == pygame.K_BACKSPACE and len(self.rendered_text.message) > 0:
            self.rendered_text.message = self.rendered_text.message[:-1]
