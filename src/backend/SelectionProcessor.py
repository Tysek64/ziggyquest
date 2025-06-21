from src.backend.Packet import Packet
from src.backend.PacketProcessor import PacketProcessor
from src.backend.Character import Character
from src.backend.PacketEnums import Command, Variable
from copy import deepcopy

# liste charaketrów z zewnatrz
class SelectorProcessor(PacketProcessor):
    def __init__(self, character_list: list[list[Character]], tier_list: list[str]) -> None:
        self.character_list = deepcopy(character_list)
        self.tier_list = tier_list
        self.teams = {}

    def process_packet(self, packet: Packet) -> list[Packet]:
        reply_packets = []
        if packet.payload[0] == Command.QUERY:
           reply_packet = Packet.generate_packet(packet.src_net, 0)
           reply_packet.payload = (Command.REPLY, None, self.get_available_characters())
           reply_packets.append(reply_packet)
        return reply_packets

    def get_available_characters(self) -> str:

        msg = "".join([
            f'{tier}: character: {character}\n'
            for tier, character_list in zip(self.tier_list, self.character_list)
                for character in character_list
        ])

        return msg
