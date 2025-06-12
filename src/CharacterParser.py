from Character import Character
import json
import os

from json import JSONDecodeError
from pathlib import Path

from Ability import Ability
from PacketEnums import Command, Team, Variable, Target, Value

class CharacterFactory:
    def make_characters(self, dir_path: Path) -> list:
        if not dir_path.exists() or not os.path.isdir(dir_path):
            raise FileNotFoundError()

        characters = []

        for file in os.listdir(dir_path):
            try:
                characters.append(self.make_character(dir_path / Path(file)))
            except JSONDecodeError:
                print(f'Character from file {file} could not be loaded!')

        return characters

    def make_character(self, json_path: Path):
        if not json_path.exists():
            raise FileNotFoundError()

        with open(json_path, mode='r') as file:
            json_file = json.load(file)

        # TODO: zmiana image ze str na image, ladowanie zdjecia bedzie tu
        return Character(
            int(json_file['checksum'], 16),
            str(json_file['image']),
            str(json_file['name']),
            int(json_file['HP']),
            int(json_file['MP']),
            int(json_file['attack']),
            int(json_file['defense']),
            int(json_file['speed']),
            self.parse_abilities(json_file['abilities'])
        )

    # packet is a list, because of json file, but it is a tuple
    def parse_packet(self, packet: list) -> tuple:
        # gdzies pomiedzy dicta i z dicta wa
        parse_dict = {
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
            'execute': Command.EXECUTE,
            'no_remain': Command.NO_REMAIN,

            'damage': Variable.DAMAGE,
            'HP': Variable.HP,
            'MP': Variable.MP,
            'attack': Variable.ATTACK,
            'defense': Variable.DEFENSE,
            'speed': Variable.SPEED,

            'default': Value.DEFAULT,
            'current': Value.CURRENT,

            None: None
        }

        return tuple([k if type(k) == int else parse_dict[k] for k in packet])

    def parse_abilities(self, abilities: list) -> list[Ability]:
        return [Ability(record['name'], int(record['cost']), None if record['trigger'] is None else self.parse_packet(record['trigger']), [self.parse_packet(packet) for packet in record['packets']]) for record in abilities]


if __name__ == '__main__':
    for character in CharacterFactory().make_characters(Path('characters')):
        print(character)