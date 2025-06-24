from pathlib import Path

from src.GUI.SurfaceRenderer import SurfaceRenderer
from src.GUI.WindowManager import WindowManager
import pygame

from src.GUI.drawables.EditableTextField import EditableTextField
from src.GUI.drawables.ResizableButton import ResizableButton
from src.GUI.drawables.ResizableImageDrawable import ResizableImageDrawable
from src.GUI.drawables.ResizableInputPopup import ResizableInputPopup
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
        (VerticalDrawable(position=pygame.Rect(480, 0, 400, parent_surface.get_height()),
                          color=pygame.Color('ivory2'), parent_surface=parent_surface,
                          contents=[
                              ResizableImageDrawable(parent_surface, Path('./src/GUI/resources/ZiggyQuest.png'),
                                                     (0,0), size=(300, 300)),
                              ResizableButton(pygame.Rect(0, 0, 200, 100), 'Singleplayer', pygame.Color('pink'),
                                              (lambda: True), parent_surface),
                              ResizableButton(pygame.Rect(0, 0, 200, 100), 'Multiplayer', pygame.Color('pink'),
                                              (lambda: True), parent_surface),
                              ResizableButton(pygame.Rect(0, 0, 200, 100), 'Exit', pygame.Color('pink'),
                                              (lambda: menu.close()), parent_surface),
                          ], row_width=1, scale_to_content=True), {}),
        (ResizableInputPopup(pygame.Rect(0, 0, 400, 200), 'Enter server ip:', pygame.Color('pink'),
                             lambda: print('cancelled'), lambda: print('accepted'), parent_surface), {}),
    ]

    for renderer in renderers:
        for render_object in render_objects:
            renderer.register(render_object)

    menu.hook_renderers(renderers)
    menu.run()
