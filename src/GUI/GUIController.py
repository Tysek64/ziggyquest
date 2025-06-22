from abc import ABCMeta, abstractmethod

class GUIController(metaclass=ABCMeta):
    def __init__(self, pygame_lock, window_width=1280, window_height=720):
        self.size = self.width, self.height = window_width, window_height
        self.pygame_lock = pygame_lock

    @abstractmethod
    def setup(self, *args, **kwargs):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def close(self):
        pass