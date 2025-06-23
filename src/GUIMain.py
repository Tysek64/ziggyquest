from src.GUI.SurfaceRenderer import SurfaceRenderer
from src.GUI.WindowManager import WindowManager
import pygame

from src.GUI.drawables.ResizableButton import ResizableButton
from src.GUI.drawables.ResizableImageDrawable import ResizableImageDrawable
from src.GUI.drawables.ResizableTextDrawable import ResizableTextDrawable
from src.GUI.drawables.VerticalDrawable import VerticalDrawable


if __name__ == '__main__':
    from threading import Lock

    menu = WindowManager(Lock())
    menu.setup()
    renderers = [
        SurfaceRenderer(pygame.display.get_surface())
    ]


    parent_surface = pygame.display.get_surface()
    render_objects = [
        (VerticalDrawable(position=pygame.Rect(480, 0, 1000, parent_surface.get_height()),
                          color=pygame.Color('ivory2'), parent_surface=parent_surface,
                          contents=[
                              ResizableTextDrawable((0,0), 'One_nig',
                                                    color=pygame.Color('red'), parent_surface=parent_surface,
                                                    centered=False),
                              ResizableButton(pygame.Rect(0, 0, 200, 100), 'Exit', pygame.Color('pink'),
                                              (lambda : menu.close()), parent_surface)
                          ], row_width=1), {})
    ]

    for renderer in renderers:
        for render_object in render_objects:
            renderer.register(render_object)

    menu.hook_renderers(renderers)
    menu.run()
