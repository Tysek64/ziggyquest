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

    TIER = auto() # for querying tier

class Value(Enum):
    DEFAULT = auto()
    CURRENT = auto()

str_to_enum = {
    'opponent': Team.OPPONENT,
    'me': Team.ME,

    'broadcast': Target.BROADCAST,
    'player_unicast': Target.PLAYER_UNICAST,
    'target_unicast': Target.TARGET_UNICAST,
    'random_unicast': Target.RANDOM_UNICAST,
    'self_unicast': Target.SELF_UNICAST,

    'set': Command.SET,
    'increase': Command.INCREASE,
    'decrease': Command.DECREASE,
    'fail': Command.FAIL,
    'execute': Command.EXECUTE,
    'no_remain': Command.NO_REMAIN,
    'end_turn': Command.END_TURN,
    'end_game': Command.END_GAME,
    'query': Command.QUERY,
    'reply': Command.REPLY,

    'damage': Variable.DAMAGE,
    'HP': Variable.HP,
    'MP': Variable.MP,
    'attack': Variable.ATTACK,
    'defense': Variable.DEFENSE,
    'speed': Variable.SPEED,
    'abilities': Variable.ABILITIES,
    'stats': Variable.STATS,
    'name': Variable.NAME,
    'character': Variable.CHARACTER,
    'ability': Variable.ABILITY,
    'tier': Variable.TIER,

    'default': Value.DEFAULT,
    'current': Value.CURRENT,

    None: None
}

enum_to_str = {v: k for k, v in str_to_enum.items()}
