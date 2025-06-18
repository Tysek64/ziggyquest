from enum import Flag, Enum, auto

class Command(Flag):
    SET = auto()
    INCREASE = auto()
    DECREASE = auto()

    EXECUTE = auto()   # for packets at turn begin
    NO_REMAIN = auto() # for packets at turn end
    END_TURN = auto()  # for committing the ending of a turn (for characters to handle accumulated damage)

    QUERY = auto()     # for querying user input
    REPLY = auto()     # for transmitting user input

class Team(Enum):
    OPPONENT = auto()
    ME = auto()

class Target(Enum):
    BROADCAST = auto()
    PLAYER_UNICAST = auto()
    TARGET_UNICAST = auto()
    RANDOM_UNICAST = auto()
    SELF_UNICAST = auto()

class Variable(Flag):
    DAMAGE = auto()
    HP = auto()
    MP = auto()
    ATTACK = auto()
    DEFENSE = auto()
    SPEED = auto()

    ABILITIES = auto() # for querying abilities
    STATS = auto()     # for querying stats
    NAME = auto()      # for querying name

class Value(Enum):
    DEFAULT = auto()
    CURRENT = auto()
