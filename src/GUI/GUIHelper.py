from src.backend.processors.PlayerProcessor import PlayerProcessor
from src.backend.processors.CharacterProcessor import CharacterProcessor
from src.backend.Packet import Packet
from typing import Callable
from src.backend.PacketEnums import Command, Variable
from src.backend.processors.SelectionProcessor import SelectionProcessor

def register_player(manager):
    def wrapper(player_creator: Callable[None, PlayerProcessor]):
        def inner(*args, **kwargs):
            def new_fn(packet: Packet):
                print(packet)
                if packet.payload is not None and packet.payload[0] == Command.QUERY:
                    reply_packet = Packet(id=None, src_net=None, dst_net=packet.src_net, dst_host=0, payload=None)
                    if packet.payload[1] == Variable.CHARACTER:
                        manager.active_team = packet.src_net if packet.src_net != -1 else packet.dst_host
                        reply_packet.payload = (Command.REPLY, None, manager.get_selected_card())
                    else:
                        manager.active_team = 0
                        reply_packet.payload = (Command.REPLY, None, manager.get_selected_ability())

                    return [reply_packet]
                elif packet.payload is not None and packet.payload[0] == Command.END_GAME:
                    if packet.payload[2] == 0:
                        manager.transfer_to_battle()
                    else:
                        manager.announce_winner(3 - packet.payload[2])
                elif packet.payload is not None and packet.payload[0] == Command.REPLY:
                    print(packet.payload[2])
                    if packet.payload[1] == Variable.CHARACTER:
                        manager.create_character(packet.src_net, packet.id, packet.payload[2])
                    else:
                        manager.create_ability(packet.payload[2])
                return []

            player = player_creator(*args, **kwargs)
            player.process_packet = new_fn
            return player
        return inner
    return wrapper
