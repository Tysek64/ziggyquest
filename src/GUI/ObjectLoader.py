import pygame
import math
from wrappers import *
class ObjectLoader:
    def __init__(self):
        pass

    # testowo, docelowo pewnie z pliku lub hard coded? Moze json skoro tak mamy postacie
    def load(self):
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
        ]