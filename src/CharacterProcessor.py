from PacketProcessor import PacketProcessor
from Character import Character
from Packet import Packet
from PacketEnums import Command, Variable, Value
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
                if self.base_character.abilities[packet.payload[2]].trigger is None:
                    #TODO : check if we can afford
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
            elif packet.payload[0] == Command.END_TURN:
                self.character_state.hp = max(0, self.character_state.hp - max(0, self.character_state.damage))
                self.character_state.damage = 0
            elif packet.payload[0] == Command.QUERY:
                if packet.payload[1] == Variable.ABILITIES:
                    for abl in self.base_character.abilities:
                        reply_packet = Packet.generate_packet(packet.src_net, 0)
                        reply_packet.payload = (Command.REPLY, 
                                                Variable.ABILITY,
                                                f'{abl.name}: {abl.cost}')

                        reply_packets.append(reply_packet)
                else:
                    reply_packet = Packet.generate_packet(packet.src_net, 0)
                    reply_packet.payload = (Command.REPLY, Variable.CHARACTER,
                                            self.base_character.name if packet.payload[1] == Variable.NAME else
                                            self.character_state)

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
