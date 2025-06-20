from PlayerProcessor import PlayerProcessor
from CharacterProcessor import CharacterProcessor
from Packet import Packet
from typing import Callable
from PacketEnums import Command, Variable
import asyncio
from GUI.CharacterCard import AbilityCard

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
                            context = manager.cards[0][1].ctx
                            manager.abilities.append((None, AbilityCard(context, res_packet.payload[2])))
                return result
            character = character_creator(*args, **kwargs)
            character._old_process_packet = character.process_packet
            character.process_packet = new_fn
            return character
        return inner
    return wrapper
