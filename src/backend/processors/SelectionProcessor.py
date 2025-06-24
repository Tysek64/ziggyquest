from src.backend.Packet import Packet
from src.backend.processors.PacketProcessor import PacketProcessor
from src.backend.character.Character import Character
from src.backend.PacketEnums import Command, Variable, Target
from copy import deepcopy

# liste charaketrów z zewnatrz
class SelectionProcessor(PacketProcessor):
    def __init__(self, character_list: list[list[Character]], tier_list: list[str]) -> None:
        self.character_list = deepcopy(character_list)
        self.tier_list = tier_list
        self.teams = {}

        self.max_team_size = 6

    def process_packet(self, packet: Packet) -> list[Packet]:
        reply_packets = []
        if packet.payload[0] == Command.QUERY:
            if packet.payload[1] == Variable.CHARACTER:
               for character in self.get_available_characters():
                   reply_packet = Packet.generate_packet(packet.src_net, 0)
                   reply_packet.payload = (Command.REPLY, Variable.TIER, character)
                   reply_packets.append(reply_packet)

            elif packet.payload[1] == Variable.TIER:
                for i, character in enumerate(self.get_characters_tier(packet.payload[2]), start=1):
                    reply_packet = Packet.generate_packet(packet.src_net, 0)
                    reply_packet.id = i
                    reply_packet.payload = (Command.REPLY, Variable.CHARACTER, character)
                    reply_packets.append(reply_packet)

        elif packet.payload[0] == Command.EXECUTE:
            team, tier, character = packet.payload[2]
            character -= 1
            try:
                self.teams[team].append(self.character_list[tier][character])
            except KeyError:
                self.teams[team] = [self.character_list[tier][character]]
            self.character_list[tier].pop(character)

        if self.notify_change_stage():
            select_end_packet = Packet.generate_packet(0, Target.BROADCAST)
            select_end_packet.payload = (Command.END_GAME, None, 0)
            reply_packets.append(select_end_packet)

        return reply_packets

    def get_available_characters(self) -> list[str]:
        return [
            f'{'-' if len(character_list) == 0 else ''} {tier}: ' + '; '.join(f'{character.name}'
                    for character in character_list
                    )            for (tier_id, tier), character_list in zip(enumerate(self.tier_list), self.character_list)
        ]

    def get_characters_tier(self, tier: int) -> list[str]:
        return [character.full_json() for character in self.character_list[tier]]


    def notify_change_stage(self) -> bool:
        exit_flag = True
        for list in self.character_list:
            if len(list) != 0:
                exit_flag = False

        if exit_flag: return True

        if len(self.teams.values()) == 0:
            return False

        for team in self.teams.values():
            if len(team) < 6:
                return False

        return True

