from functools import singledispatch

from src.GUI.drawables.Drawable import Drawable
from src.GUI.wrappers import *

def auto_draw(surface: pygame.Surface,
              drawable, *args, **kwargs) -> None:
    return _drawing_dispatch(drawable, surface, *args, **kwargs)


@singledispatch
def _drawing_dispatch(drawable, surface, *args, **kwargs):
    print(drawable)
    raise NotImplemented()

@_drawing_dispatch.register(pygame.Rect)
def _(drawable, surface, *args, **kwargs):
    pygame.draw.rect(*args, **kwargs, surface=surface, rect=drawable)

@_drawing_dispatch.register(Polygon)
def _(polygon, surface, *args, **kwargs):
    pygame.draw.polygon(*args, **kwargs | polygon.to_dict(), surface=surface)

@_drawing_dispatch.register(Circle)
def _(circle, surface, *args, **kwargs):
    pygame.draw.circle(*args, **kwargs | circle.to_dict(), surface=surface)

@_drawing_dispatch.register(Ellipse)
def _(ellipse, surface, *args, **kwargs):
    pygame.draw.ellipse(*args, **kwargs | ellipse.to_dict(), surface=surface)

@_drawing_dispatch.register(Arc)
def _(arc, surface, *args, **kwargs):
    pygame.draw.arc(*args, **kwargs | arc.to_dict(), surface=surface)

@_drawing_dispatch.register(Line)
def _(line, surface, *args, **kwargs):
    pygame.draw.line(*args, **kwargs | line.to_dict(), surface=surface)

@_drawing_dispatch.register(Lines)
def _(lines, surface, *args, **kwargs):
    pygame.draw.lines(*args, **kwargs | lines.to_dict(), surface=surface)

@_drawing_dispatch.register(AALine)
def _(aaline, surface, *args, **kwargs):
    pygame.draw.aaline(*args, **kwargs | aaline.to_dict(), surface=surface)

@_drawing_dispatch.register(Lines)
def _(aalines, surface, *args, **kwargs):
    pygame.draw.aalines(*args, **kwargs | aalines.to_dict(), surface=surface)

@_drawing_dispatch.register(pygame.Surface)
def _(inner_surface, surface, *args, **kwargs):
    surface.blit(*args, **kwargs, source=inner_surface)

@_drawing_dispatch.register(Drawable)
def _(drawable, surface, *args, **kwargs):
    drawable.draw(surface, *args, **kwargs)
