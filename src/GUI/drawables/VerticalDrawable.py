from src.GUI.draw_utils import auto_draw
from src.GUI.drawables.CompositeMixin import CompositeMixin
from src.GUI.drawables.Drawable import Drawable
from src.GUI.drawables.ResizeMixin import ResizeMixin
import pygame
class VerticalDrawable(ResizeMixin, CompositeMixin, Drawable):
    def __init__(self,
                 position: pygame.Rect,
                 color: pygame.Color,
                 parent_surface: pygame.Surface,
                 contents=None,
                 row_width: int = 2,
                 scale_to_content: bool = True):
        self.__inner_left_margin = position.width // 10
        self.__inner_top_margin = 20
        self.margins = (self.__inner_left_margin, self.__inner_top_margin)
        self.position = position
        self.color = color
        self.parent_surface = parent_surface
        # element position
        self.points: list[tuple[int, int]] = []
        self.drawables: list[pygame.Surface] = []
        self.contents = contents
        self.row_width = row_width
        self.scale_to_content = scale_to_content
        self._rendered_objects = []

        if contents is not None:
            for element in contents:
                self.add(element)

        super().__init__(points=['position', 'points', 'margins'], surfaces=['drawables'], parent_surface=parent_surface)

    def add(self, element: Drawable):
        size = element.get_rect().size
        new_index = len(self.drawables)
        new_pos = (self.position.x + self.__inner_left_margin, self.position.y + self.__inner_top_margin)
        new_surface = pygame.Surface(size,  pygame.SRCALPHA)
        new_surface.fill((0, 0, 0, 0))

        if new_index > 0:
            last_element_surface = self.drawables[-1]
            last_position = self.points[-1]
            if new_index % self.row_width == 0:
                new_pos = ( self.position.x + self.__inner_left_margin,
                            last_position[1] + last_element_surface.get_rect().bottomleft[1] + self.__inner_top_margin)
            else:
                new_pos = (last_position[0] + last_element_surface.get_rect().topright[0] + self.__inner_left_margin,
                           last_position[1] + last_element_surface.get_rect().y)

        self._rendered_objects.append(element)
        self.drawables.append(new_surface)
        self.points.append(new_pos)
        if self.scale_to_content:
            row_list = [self.drawables[i:i + self.row_width] for i in range(0, len(self.drawables), self.row_width)]
            max_row_sum = max([sum([drawable.get_width() for drawable in row]) for row in row_list])
            self.position.size = (max_row_sum + (self.row_width + 1) * self.__inner_left_margin, self.position.size[1])



        self.reinit(self.parent_surface, ['position', 'points'], ['drawables'])


    def draw(self, surface, *args, **kwargs):
        self.resize()
        auto_draw(surface, self.position, color=self.color)
        for (element, inner_surface), position in zip(zip(self._rendered_objects, self.drawables), self.points):
            auto_draw(inner_surface, element)
            auto_draw(surface, inner_surface, dest=position)



    def get_rect(self) -> pygame.Rect:
        return self.position