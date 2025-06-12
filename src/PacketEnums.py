from enum import Enum, auto


class Command(Enum):
    SET = auto()
    INCREASE = auto()
    DECREASE = auto()

    EXECUTE = auto()   # for packets at turn begin
    NO_REMAIN = auto() # for packets at turn end

class Team(Enum):
    OPPONENT = auto()
    ME = auto()

class Target(Enum):
    BROADCAST = auto()
    PLAYER_UNICAST = auto()
    TARGET_UNICAST = auto()
    RANDOM_UNICAST = auto()
    SELF_UNICAST = auto()

class Variable(Enum):
    DAMAGE = auto()
    HP = auto()
    MP = auto()
    ATTACK = auto()
    DEFENSE = auto()
    SPEED = auto()

class Value(Enum):
    DEFAULT = auto()
    CURRENT = auto()