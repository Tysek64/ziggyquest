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
                print('Hello from new function!')
                if packet.payload is not None and packet.payload[0] == Command.QUERY:
                    print(packet)
                    reply_packet = Packet(id=None, src_net=None, dst_net=packet.src_net, dst_host=0, payload=None)
                    if packet.payload[1] == Variable.CHARACTER:
                        manager.active_team = packet.src_net if packet.src_net != -1 else packet.dst_host
                        reply_packet.payload = (Command.REPLY, None, manager.get_selected_card())
                    else:
                        manager.active_team = 0
                        reply_packet.payload = (Command.REPLY, None, manager.get_selected_ability())

                    return [reply_packet]
                elif packet.payload is not None and packet.payload[0] == Command.END_GAME:
                    manager.announce_winner(3 - packet.dst_host)
                return []

            player = player_creator(*args, **kwargs)
            player.process_packet = new_fn
            return player
        return inner
    return wrapper

def register_character(manager):
    def wrapper(character_creator: Callable[None, CharacterProcessor]):
        def inner(*args, **kwargs):
            def new_fn(packet: Packet):
                result = character._old_process_packet(packet)
                for res_packet in result:
                    if res_packet.payload[0] == Command.REPLY:
                        if res_packet.payload[1] == Variable.ABILITY:
                            manager.create_ability(res_packet.payload[2])
                return result
            character = character_creator(*args, **kwargs)
            character._old_process_packet = character.process_packet
            character.process_packet = new_fn
            return character
        return inner
    return wrapper

def register_selection(manager):
    def wrapper(selection_creator: Callable[None, SelectionProcessor]):
        def inner(*args, **kwargs):
            def new_fn(packet: Packet):
                result = character._old_process_packet(packet)
                for res_packet in result:
                    if res_packet.payload[0] == Command.REPLY:
                        if res_packet.payload[1] == Variable.TIER:
                            manager.create_tier(res_packet.payload[2])
                        else:
                            manager.create_character(res_packet.payload[2])
                return result
            character = selection_creator(*args, **kwargs)
            character._old_process_packet = character.process_packet
            character.process_packet = new_fn
            return character
        return inner
    return wrapper
