from src.backend.BaseRouter import BaseRouter
from src.backend.NetInfo import NetInfo
from src.backend.Packet import Packet
from src.backend.PacketEnums import Command, Target, Variable

class SelectionRouter(BaseRouter):
    def __init__(self, net_info: NetInfo, hostname: str | None = None):
        super().__init__(net_info, hostname)
        # tier, character_id
        self.current_move = (None, None, None)

    def handshake(self):
        self.handshake_running = True
        self.current_move = (self.current_team, None, None)

        self.finished_turn = [True for _ in self.finished_turn]

        packet = Packet.generate_packet(1, 1)
        packet.payload = (Command.QUERY, Variable.CHARACTER, None)
        self.send_packet(packet)

        packet = Packet.generate_packet(0, self.current_team)
        packet.payload = (Command.QUERY, None, 'Input character tier: ')
        self.send_packet(packet)

        self.finished_turn = [True for _ in self.finished_turn]
        self.handshake_running = False

    def end_turn(self):
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
            if self.current_move[2] is not None and sum(self.finished_turn) == len(self.finished_turn):
                #print(f'For {self}, the turn is over!\n')
                self.end_turn()
        elif packet.payload is not None and packet.payload[0] == Command.REPLY and packet.src_net != 0:
            print(packet.payload[2])
        else: # REPLY from player
            if self.current_move[1] is None:
                self.current_move = (self.current_move[0], packet.payload[2], None)
                packet_ = Packet.generate_packet(1, 1)
                packet_.payload = (Command.QUERY, Variable.TIER, packet.payload[2])
                self.send_packet(packet_)

                packet = Packet.generate_packet(0, self.current_team)
                packet.payload = (Command.QUERY, None, 'Input character ID: ')
                self.send_packet(packet)


            elif self.current_move[2] is None:
                self.current_move = (self.current_move[0], self.current_move[1], packet.payload[2])
                packet = Packet.generate_packet(1, 1)
                packet.payload = (Command.EXECUTE, None, self.current_move)
                self.send_packet(packet)

