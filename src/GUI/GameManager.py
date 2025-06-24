from enum import Enum, auto

from src.GUI.GUIBattle import GUIBattleManager
from src.backend.character.Character import Character
from src.GUI.GUIController import GUIController
from functools import wraps
from threading import Lock

class GameStage(Enum):
    MENU = auto()
    SELECTION = auto()
    BATTLE = auto()


class GameManager:
    def __init__(self) -> None:
        self.current_stage = GameStage.MENU
        self.pygame_lock = Lock()
        self.controller_object = None

    def get_lock(self):
        return self.pygame_lock

    def set_controller(self, controller_object: GUIController):
        self.controller_object = controller_object


    def change_to_battle(self):
        self.controller_object.close()
        print('change to battle')


