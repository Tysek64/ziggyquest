from enum import Flag, Enum, auto

class Command(Flag):
    SET = auto()
    INCREASE = auto()
    DECREASE = auto()

    FAIL = auto()      # for communicating failure in execution
    EXECUTE = auto()   # for packets at turn begin
    NO_REMAIN = auto() # for packets at turn end
    END_TURN = auto()  # for committing the ending of a turn (for characters to handle accumulated damage)
    END_GAME = auto()  # for signalling the death of a character and the whole team

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

    CHARACTER = auto() # for querying character id
    ABILITY = auto()   # for querying ability id

class Value(Enum):
    DEFAULT = auto()
    CURRENT = auto()
