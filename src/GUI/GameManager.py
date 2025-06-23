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

    def set_controller(self, controller_object):
        self.controller_object = controller_object


    def change_controller(self, state, *args, **kwargs):
        self.controller_object.close()
        if state == GameStage.BATTLE:
            self.controller_object = GUIBattleManager(self.pygame_lock)
            self.controller_object.setup_battle(kwargs['team1'], kwargs['team2'])
            self.controller_object.run_battle()
            self.controller_object.close()



def change_to_battle(context):
    def register_(cls):
        old_fun = cls.notify_change_stage
        @wraps(old_fun)
        def inner(*args, **kwargs):
            if old_fun(*args, **kwargs):
                print(cls.teams, cls.character_list)
                context.init_battle(list(cls.teams.values()))
            return old_fun(*args, **kwargs)
        cls.notify_change_stage = inner
        return cls
    return register_