from src.backend.net_devices.BaseRouter import BaseRouter
from src.backend.NetInfo import NetInfo
from src.backend.Packet import Packet
from src.backend.PacketEnums import Command, Target, Variable

class BattleRouter(BaseRouter):
    def __init__(self, net_info: NetInfo, hostname: str | None = None):
        super().__init__(net_info, hostname)
        self.current_move = (False, None, None)

    def handshake(self):
        if self.current_move[0] == False:
            self.current_move = (True, None, None)
            self.finished_turn = [True for i in self.finished_turn]

            self.query_character()

    def end_turn(self):
        self.current_move = (False, None, None)

        for port in self.ports:
            end_turn_packet = Packet.generate_packet(port.address.net_addr, Target.BROADCAST)
            end_turn_packet.payload = (Command.END_TURN, None, None)
            port.send_packet(end_turn_packet, sender=self)

        self.current_team = 3 - self.current_team
        print(f'END TURN! The current team is {self.current_team}')

    def process_packet(self, packet: Packet):
        #print(f'{self} received {packet}')
        if packet.payload is not None and packet.payload[0] == Command.NO_REMAIN:
            self.finished_turn[packet.src_net] = True
            if self.current_move[1] is not None and self.current_move[2] is not None and sum(self.finished_turn) == len(self.finished_turn):
                #print(f'For {self}, the turn is over!\n')
                self.end_turn()
        elif packet.payload is not None and packet.payload[0] == Command.FAIL:
            self.current_move = (False, None, None)
        elif packet.payload is not None and packet.payload[0] == Command.REPLY:
            if packet.src_net != 0:
                relay_packet = Packet.generate_packet(0, Target.BROADCAST if packet.payload[1] != Variable.ABILITY else self.current_team)
                relay_packet.id = packet.id
                relay_packet.src_net = packet.src_net
                relay_packet.payload = packet.payload
                self.receive_packet(relay_packet)
            else:
                if self.current_move[1] is None:
                    self.current_move = (True, packet.payload[2], None)
                    self.query_ability()
                elif self.current_move[2] is None:
                    self.current_move = (True, self.current_move[1], packet.payload[2])

                    start_turn_packet = Packet.generate_packet(self.current_team, self.current_move[1])
                    start_turn_packet.payload = (Command.EXECUTE, None, self.current_move[2])

                    self.finished_turn[self.current_team] = False
                    self.send_packet(start_turn_packet)
                else:
                    raise ValueError(f'Router {self} received a reply to no asked questions: {packet}')
        elif packet.payload is not None and packet.payload[0] == Command.END_GAME:
            end_game_packet = Packet.generate_packet(0, Target.BROADCAST)
            end_game_packet.payload = (Command.END_GAME, None, packet.src_net)

            self.send_packet(end_game_packet)
        else:
            raise ValueError(f'Router {self} received {packet} for some reason')

    def query_character(self):
        packet = Packet.generate_packet(self.current_team, Target.BROADCAST)
        packet.payload = (Command.QUERY, Variable.STATS, "")
        self.send_packet(packet)

        packet = Packet.generate_packet(3 - self.current_team, Target.BROADCAST)
        packet.payload = (Command.QUERY, Variable.NAME, "")
        self.send_packet(packet)

        packet = Packet.generate_packet(0, self.current_team)
        packet.payload = (Command.QUERY, Variable.CHARACTER, 'Input character ID: ')
        self.send_packet(packet)

    def query_ability(self):
        packet = Packet.generate_packet(self.current_team, self.current_move[1])
        packet.payload = (Command.QUERY, Variable.ABILITIES, "")
        self.send_packet(packet)

        packet = Packet.generate_packet(0, self.current_team)
        packet.payload = (Command.QUERY, Variable.ABILITY, 'Input ability ID: ')
        self.send_packet(packet)
