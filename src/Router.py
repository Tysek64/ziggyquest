from Packet import Packet
from PacketEnums import Command
from Connection import Connection
from Inteface import Interface
from NetDevice import NetDevice
from NetInfo import NetInfo
class Router(NetDevice):
    def __init__(self, net_info: NetInfo, hostname: str | None = None):
        self.ports: list[Interface] = []
        self.net_info = net_info
        self.hostname = hostname

        self.current_team = 1
        self.current_move = (None, None)

    def __str__(self):
        return self.hostname if self.hostname is not None else super.__str__(self)

    def add_interface(self, interface: Interface):
        self.ports.append(interface)

    def handshake(self):
        packet = Packet.generate_packet(0, self.current_team)
        packet.payload = (Command.QUERY, None, 'Input character ID: ')
        self.send_packet(packet)

        packet = Packet.generate_packet(0, self.current_team)
        packet.payload = (Command.QUERY, None, 'Input ability ID: ')
        self.send_packet(packet)

    def process_packet(self, packet: Packet):
        print(f'{self} received {packet}')
        if self.current_move[0] is None:
            self.current_move = (packet.payload[2], None)
        elif self.current_move[1] is None:
            self.current_move = (self.current_move[0], packet.payload[2])

            start_turn_packet = Packet.generate_packet(self.current_team, self.current_move[0])
            start_turn_packet.payload = (Command.EXECUTE, None, self.current_move[1])

            self.send_packet(start_turn_packet)
            self.current_move = (None, None)
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
                    port.send_packet(packet, sender=self)
                    success = True
        if not success:
            self.process_packet(packet)
