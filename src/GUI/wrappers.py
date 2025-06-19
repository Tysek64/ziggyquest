from dataclasses import dataclass
import pygame

def dict_decorator(cls):
    def to_dict(self) -> dict:
        return self.__dict__

    cls.to_dict = to_dict
    return cls

@dict_decorator
@dataclass
class Polygon:
    points: list[tuple[int, int]]

@dict_decorator
@dataclass
class Circle:
    center: tuple[int, int]
    radius: int

@dict_decorator
@dataclass
class Ellipse:
    rect: pygame.Rect

@dict_decorator
@dataclass
class Arc:
    rect: pygame.Rect
    start_angle: float
    stop_angle: float

@dict_decorator
@dataclass
class Line:
    start_pos: tuple[int, int]
    end_pos: tuple[int, int]

@dict_decorator
@dataclass
class Lines:
    points: list[tuple[int, int]]
    closed: bool

class AALine(Line): pass
class AALines(Lines): pass

