from src.GUI.GameManager import GameManager
from src.GUI.SurfaceRenderer import SurfaceRenderer
import pygame

def setup_game(drawables):
    game = GameManager(1000, 800)
    game.setup_game()
    renderers = [
        SurfaceRenderer(pygame.display.get_surface())
    ]

    render_objects = [(con, {}) for con in drawables]
    for renderer in renderers:
        for render_object in render_objects:
            renderer.register(render_object)

    game.hook_renderers(renderers)
    game.run_game()