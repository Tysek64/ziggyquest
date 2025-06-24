import pygame
from copy import deepcopy

# tylko dwie osoby wiedza co ten kod robi - Bog i ja xD

# main surface - surface to follow
class ResizeMixin:
    def __init__(self, parent_surface: pygame.Surface, points: list[str], surfaces: list[str],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_surface = parent_surface
        self.begin_size = parent_surface.get_size()
        self.begin_points = {attrib_name: deepcopy(self.__getattribute__(attrib_name)) for attrib_name in points}
        self.__points = points
        self.__surfaces = surfaces
        self.begin_surfaces = None
        self.copy_surfaces(surfaces)

    def copy_surfaces(self, attrib_names: list[str]):
        self.begin_surfaces = {attrib_name: self.__getattribute__(attrib_name) for attrib_name in attrib_names}
        for name, surface in self.begin_surfaces.items():
            if isinstance(surface, pygame.Surface):
                self.begin_surfaces[name] = surface.copy()
            elif isinstance(surface, list):
                self.begin_surfaces[name] = [inner_surface.copy() for inner_surface in surface]

    def reinit(self, parent_surface: pygame.Surface, points: list[str], surfaces: list[str]):
        self.__points = points
        self.__surfaces = surfaces
        self.main_surface = parent_surface
        self.begin_size = parent_surface.get_size()
        self.begin_points = {attrib_name: deepcopy(self.__getattribute__(attrib_name)) for attrib_name in points}
        self.copy_surfaces(surfaces)


    def resize(self):
        current_size = self.main_surface.get_size()
        x_scale, y_scale = current_size[0] / self.begin_size[0], current_size[1] / self.begin_size[1]
        for attrib_name in self.__points:
            # single dispatch, single dispatch !
            if isinstance(self.__getattribute__(attrib_name), tuple):
                point = self.begin_points[attrib_name]
                self.__setattr__(attrib_name, (round(point[0] * x_scale), round(point[1] * y_scale)))
            elif isinstance(self.__getattribute__(attrib_name), list):
                point_list = self.__getattribute__(attrib_name)
                begin_point_list = self.begin_points[attrib_name]
                for i in range(len(point_list)):
                    point_list[i] = begin_point_list[i][0] * x_scale, begin_point_list[i][1] * y_scale
            elif isinstance(self.__getattribute__(attrib_name), pygame.Rect):
                rect = self.begin_points[attrib_name]
                rect = pygame.Rect(round(rect.x * x_scale),
                    round(rect.y * y_scale),
                    round(rect.width * x_scale),
                    round(rect.height * y_scale))
                self.__setattr__(attrib_name, rect)



        for attrib_name in self.__surfaces:
            surfaces = self.begin_surfaces[attrib_name]
            if isinstance(self.__getattribute__(attrib_name), pygame.Surface):
                surface = self.begin_surfaces[attrib_name]
                width, height = surface.get_size()
                new_surface_size = (width * x_scale, height * y_scale)
                self.__setattr__(attrib_name, pygame.transform.scale(surface, new_surface_size))
            elif isinstance(self.__getattribute__(attrib_name), list):
                for i in range(len(surfaces)):
                    begin_surface = surfaces[i]
                    width, height = begin_surface.get_size()
                    new_surface_size = (width * x_scale, height * y_scale)
                    self.__getattribute__(attrib_name)[i] = pygame.transform.scale(begin_surface, new_surface_size)

        self.current_size = current_size
