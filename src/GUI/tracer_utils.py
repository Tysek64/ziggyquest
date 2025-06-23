from src.GUI.WindowManager import WindowManager
from src.GUI.SurfaceRenderer import SurfaceRenderer
import pygame

def setup_game(game: WindowManager, drawables):
    renderers = [
        SurfaceRenderer(pygame.display.get_surface())
    ]

    render_objects = [(con, {}) for con in drawables]
    for renderer in renderers:
        for render_object in render_objects:
            renderer.register(render_object)

    game.hook_renderers(renderers)
    game.run()