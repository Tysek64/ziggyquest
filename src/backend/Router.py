from src.backend.Connection import Connection
from src.backend.Inteface import Interface
from src.backend.NetDevice import NetDevice
from src.backend.NetInfo import NetInfo
from src.backend.Packet import Packet
from src.backend.PacketEnums import Command, Target, Variable

class Router(NetDevice):
    def __init__(self, net_info: NetInfo, hostname: str | None = None):
        self.ports: list[Interface] = []
        self.net_info = net_info
        self.hostname = hostname

        self.current_team = 1
        self.current_move = (False, None, None)

        self.finished_turn = []

    def __str__(self):
        return self.hostname if self.hostname is not None else super.__str__(self)

    def add_interface(self, interface: Interface):
        self.ports.append(interface)
        self.finished_turn.append(True)

    def handshake(self):
        if self.current_move[0] == False:
            self.current_move = (True, self.current_move[1], self.current_move[2])
            self.finished_turn = [True for i in self.finished_turn]

            packet = Packet.generate_packet(self.current_team, Target.BROADCAST)
            packet.payload = (Command.QUERY, Variable.STATS, "")
            self.send_packet(packet)

            packet = Packet.generate_packet(3 - self.current_team, Target.BROADCAST)
            packet.payload = (Command.QUERY, Variable.NAME, "")
            self.send_packet(packet)

            packet = Packet.generate_packet(0, self.current_team)
            packet.payload = (Command.QUERY, Variable.CHARACTER, 'Input character ID: ')
            self.send_packet(packet)

            self.finished_turn = [True for i in self.finished_turn]

    def selection_handshake(self):
        self.finished_turn = [True for _ in self.finished_turn]

        packet = Packet.generate_packet(1, 1)
        packet.payload = (Command.QUERY, None, "")
        self.send_packet(packet)

        packet = Packet.generate_packet(0, self.current_team)
        packet.payload = (Command.QUERY, Variable.CHARACTER, 'Input character name: ')
        self.send_packet(packet)

        self.finished_turn = [True for _ in self.finished_turn]

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
        elif packet.payload is not None and packet.payload[0] == Command.REPLY and packet.src_net != 0:
            print(packet.payload[2])
        else:
            if self.current_move[1] is None:
                self.current_move = (True, packet.payload[2], None)

                packet = Packet.generate_packet(self.current_team, self.current_move[1])
                packet.payload = (Command.QUERY, Variable.ABILITIES, "")
                self.send_packet(packet)

                packet = Packet.generate_packet(0, self.current_team)
                packet.payload = (Command.QUERY, Variable.ABILITY, 'Input ability ID: ')
                self.send_packet(packet)

            elif self.current_move[2] is None:
                self.current_move = (True, self.current_move[1], packet.payload[2])

                start_turn_packet = Packet.generate_packet(self.current_team, self.current_move[1])
                start_turn_packet.payload = (Command.EXECUTE, None, self.current_move[2])

                self.finished_turn[self.current_team] = False
                self.send_packet(start_turn_packet)
            else:
                raise ValueError(f'Router {self} received a reply to no asked questions')

    def send_packet(self, packet: Packet):
        packet.src_net = self.net_info.net_addr
        self.receive_packet(packet)

    def receive_packet(self, packet: Packet):
        success = False
        for port in self.ports:
            if port.address.net_addr == packet.dst_net:
                if success:
                    raise ConnectionError(f'Two networks with the same address connected to router {self}')
                else:
                    self.finished_turn[port.address.net_addr] = False
                    port.send_packet(packet, sender=self)
                    success = True
        if not success:
            self.process_packet(packet)
