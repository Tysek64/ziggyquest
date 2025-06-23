from src.backend.processors.PacketProcessor import PacketProcessor
from src.backend.character.Character import Character
from src.backend.Packet import Packet
from src.backend.PacketEnums import Command, Variable, Value, Target
from copy import deepcopy

# holds state and responds to packets
class CharacterProcessor(PacketProcessor):
    def __init__(self, base_character: Character) -> None:
        self.base_character = base_character
        self.character_state = deepcopy(base_character)
        self.character_state.damage = 0
 
        self.attr_map = {
            Variable.DAMAGE: ('damage', 0, float('inf')),
            Variable.HP: ('hp', 0, self.base_character.hp),
            Variable.MP: ('mp', 0, self.base_character.mp),
            Variable.ATTACK: ('attack', 0, float('inf')),
            Variable.DEFENSE: ('defense', 0, float('inf')),
            Variable.SPEED: ('speed', 0, float('inf')),
        }

        self.trigger_queue = {}
    
    def match_packet(self, packet: Packet, pattern: tuple) -> bool:
        cmd, var = pattern
        return (cmd is None or packet.payload[0] == cmd) and (var is None or packet.payload[1] == var)

    def process_packet(self, packet: Packet) -> list[Packet]: 
        reply_packets = []

        if packet.payload is not None:
            if packet.payload[0] == Command.EXECUTE:
                if self.character_state.hp == 0:
                    # fail if character is dead
                    reply_packet = Packet.generate_packet(-1, 0)
                    reply_packet.payload = (Command.FAIL, Variable.CHARACTER, None)
                    reply_packets.append(reply_packet)
                else:
                    if self.base_character.abilities[packet.payload[2]].cost <= self.character_state.mp:
                        self.character_state.mp -= self.base_character.abilities[packet.payload[2]].cost
                        if self.base_character.abilities[packet.payload[2]].trigger is None:
                            for step in self.base_character.abilities[packet.payload[2]].packets:
                                new_packet = Packet.make_packet(step)
                                new_payload = list(new_packet.payload)

                                if new_packet.payload[2] == Value.CURRENT:
                                    new_payload[2] = getattr(self.character_state, self.attr_map[new_packet.payload[1]][0])
                                elif new_packet.payload[2] == Value.DEFAULT:
                                    new_payload[2] = getattr(self.base_character, self.attr_map[new_packet.payload[1]][0])

                                new_packet.payload = new_payload

                                reply_packets.append(new_packet)
                        else:
                            queued_packets = self.trigger_queue.get(self.base_character.abilities[packet.payload[2]].trigger, [])
                            queued_packets.extend(self.base_character.abilities[packet.payload[2]].packets)
                            # creates key if it did not exist
                            self.trigger_queue[self.base_character.abilities[packet.payload[2]].trigger] = queued_packets
                    else:
                        # fail if ability is too expensive
                        reply_packet = Packet.generate_packet(-1, 0)
                        reply_packet.payload = (Command.FAIL, Variable.ABILITY, None)
                        reply_packets.append(reply_packet)
            elif packet.payload[0] == Command.END_TURN:
                self.character_state.hp = max(0, self.character_state.hp - max(0, self.character_state.damage))
                self.character_state.damage = 0

                if self.character_state.hp == 0:
                    reply_packet = Packet.generate_packet(packet.dst_net, 0)
                    reply_packet.payload = (Command.END_GAME, None, None)
                    reply_packets.append(reply_packet)
            elif packet.payload[0] == Command.QUERY:
                if packet.payload[1] == Variable.ABILITIES:
                    for abl in self.base_character.abilities:
                        reply_packet = Packet.generate_packet(packet.src_net, Target.BROADCAST)
                        reply_packet.payload = (Command.REPLY, Variable.ABILITY, f'{'-' if abl.cost > self.character_state.mp else ''} {abl.name}: {abl.cost}')

                        reply_packets.append(reply_packet)
                else:
                    reply_packet = Packet.generate_packet(packet.src_net, Target.BROADCAST)
                    reply_packet.payload = (Command.REPLY, Variable.CHARACTER,
                                            #self.base_character.name if packet.payload[1] == Variable.NAME else
                                            self.character_state.__repr__())

                    reply_packets.append(reply_packet)
            elif packet.payload[0] in (Command.SET, Command.INCREASE, Command.DECREASE):
                if packet.payload[1] in self.attr_map:
                    attr_name, minimum, maximum = self.attr_map[packet.payload[1]]
                    current_val = getattr(self.character_state, attr_name)
                    amount = packet.payload[2]

                    if packet.payload[0] == Command.SET:
                        new_val = amount
                    elif packet.payload[0] == Command.INCREASE:
                        new_val = current_val + amount
                    elif packet.payload[0] == Command.DECREASE:
                        new_val = current_val - amount

                    if packet.payload[1] == Variable.ATTACK:
                        self.base_character.damage = new_val * 3

                    setattr(self.character_state, attr_name, max(min(new_val, maximum), minimum))

                for k, v in self.trigger_queue.items():
                    if self.match_packet(packet, k):
                        for step in v:
                            new_packet = Packet.make_packet(step)
                            new_payload = list(new_packet.payload)

                            if new_packet.payload[2] == Value.CURRENT:
                                new_payload[2] = getattr(self.character_state, self.attr_map[new_packet.payload[1]][0])
                            elif new_packet.payload[2] == Value.DEFAULT:
                                new_payload[2] = getattr(self.base_character, self.attr_map[new_packet.payload[1]][0])

                            new_packet.payload = new_payload

                            reply_packets.append(new_packet)
                        self.trigger_queue[k] = []

        return reply_packets
