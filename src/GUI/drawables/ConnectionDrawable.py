import pygame

from src.backend.Connection import Connection
from src.GUI.draw_utils import auto_draw
from src.GUI.drawables.Drawable import Drawable

from src.GUI.drawables.ImageDrawable import ImageDrawable
from src.GUI.wrappers import Line
from pathlib import Path
from functools import wraps
from time import sleep
import numpy as np

class ConnectionDrawable(Drawable):

    def __init__(self, begin: tuple[int, int], end: tuple[int, int]):
        self.line = Line(begin, end)
        self.monitored_connection = None
        self.simulation_speed = 3
        self.max_tick = 255
        self.current_tick = 0

        self.packet_img = None
        self.traverse_time = self.max_tick / self.simulation_speed
        self.send_vector = np.array([float(end[0] - begin[0]), float(end[1] - begin[1])]) / self.traverse_time
        self.current_vector = np.array([0.,0.])

    def connect(self, connection: Connection):

        old_fun = connection.transfer_packet
        @wraps(old_fun)
        def wrapper(sender, packet):
            self.notify(sender, packet)
            sleep(5)
            old_fun(sender, packet)

        connection.transfer_packet = wrapper

        self.monitored_connection = connection

    def notify(self, sender, packet):
        self.current_tick = 255
        self.packet_img = ImageDrawable(Path('D:/python_laby/ziggyquest/src/GUI/resources/packet.png'),
                                        position=self.line.start_pos)
        self.packet_img.background_color = pygame.Color(0,0,255)
        if sender is self.monitored_connection.begin:
            self.packet_img.position = self.line.start_pos
            self.current_vector = self.send_vector
        else:
            self.packet_img.position = self.line.end_pos
            self.current_vector = -self.send_vector

        #print('notified')

    def draw(self, surface, *args, **kwargs):
        auto_draw(surface, self.line, color=pygame.Color(255 - self.current_tick, self.current_tick , 0))

        self.current_tick = max(0, self.current_tick-self.simulation_speed)
        if self.packet_img is not None:
            auto_draw(surface, self.packet_img)
            self.packet_img.position = tuple(self.packet_img.position + self.current_vector)
            if self.current_tick == 0:
                self.packet_img = None
                self.current_vector = None
