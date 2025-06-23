import pygame
import math

from src.GUI.drawables.ResizableImageDrawable import ResizableImageDrawable
from src.GUI.drawables.ResizableTextDrawable import ResizableTextDrawable
from src.GUI.drawables.TierCard import TierCard
from src.GUI.drawables.VerticalDrawable import VerticalDrawable
from src.GUI.wrappers import *
from src.GUI.drawables.ImageDrawable import ImageDrawable

from pathlib import Path
class ObjectLoader:
    def __init__(self):
        pass

    # testowo, docelowo pewnie z pliku lub hard coded? Moze json skoro tak mamy postacie
    def load(self, parent_surface: pygame.Surface, test_object):
        return [
            (pygame.Rect(0, 0, 50, 100), {
                'color': pygame.Color(255,255,255)
            }),

            (Arc(pygame.Rect(30, 20, 200, 100), 0, math.pi/3), {
                'color': pygame.Color(255, 0, 0),
                'width': 30
            }),

            (Line((50, 100), (512, 200)), {
                'color': pygame.Color(0, 255, 0),
                'width': 3
            }),

            (AALine((100, 150), (562, 250)), {
                'color': pygame.Color(0, 255, 0),
            }),

            (AALines([(300, 300), (400, 250), (500, 300)], True), {
                'color': pygame.Color(0, 255, 0),
            }),

            (ImageDrawable(Path('D:/python_laby/ziggyquest/src/GUI/resources/Host.jpg'),
                           (250, 250), (100, 100)), {}),

            (ResizableImageDrawable(pygame.display.get_surface(),
                                    Path('D:/python_laby/ziggyquest/src/GUI/resources/Host.jpg'),
                           (350, 350), (100, 100)), {}),
            (ResizableTextDrawable((500, 300), 'Sog4y', pygame.Color(128, 128, 128), parent_surface),{}),
            (VerticalDrawable(pygame.Rect(200, 100, 400, parent_surface.get_rect().height), color=pygame.Color('ivory3'), parent_surface=parent_surface, row_width=3,
                              contents=[
                                  TierCard(test_object, pygame.Rect(0, 0, 300, 400), pygame.Color(0, 0, 255),
                                            parent_surface),
                                  TierCard(test_object, pygame.Rect(0, 0, 300, 400), pygame.Color(0, 0, 255),
                                           parent_surface),
                                  TierCard(test_object, pygame.Rect(0, 0, 300, 400), pygame.Color(0, 0, 255),
                                           parent_surface),
                                  TierCard(test_object, pygame.Rect(0, 0, 300, 400), pygame.Color(0, 0, 255),
                                           parent_surface)
                              ]), {}),

        ]