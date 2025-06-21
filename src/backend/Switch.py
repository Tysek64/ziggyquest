from src.backend.Connection import Connection
from src.backend.Inteface import Interface
from src.backend.NetDevice import NetDevice
from src.backend.NetInfo import NetInfo
from src.backend.Packet import Packet
from src.backend.PacketEnums import Target, Command, Team, Variable
import random

class Switch(NetDevice):
    def __init__(self, net_info: NetInfo, hostname=None):
        self.net_info = net_info
        self.ports: list[Interface] = []
        self.router = None
        self.hostname = hostname
        self.packet_queue: list[Packet] = []

        self.remaining_nonanswered = 0
        self.dead_characters = 0

    def __str__(self):
        return self.hostname if self.hostname is not None else super.__str__(self)

    def add_interface(self, interface: Interface):
        self.ports.append(interface)
        self.remaining_nonanswered = 0

    def connect_router(self, interface: Interface):
        self.router = interface

    def process_packet(self, packet: Packet):
        #print(f'{self} received {packet}')
        if packet.payload is not None and packet.payload[0] == Command.REPLY:
            try:
                forward_packet = self.packet_queue.pop(0)
            except IndexError:
                raise ValueError(f'Switch {self} received a reply to no asked questions')
            forward_packet.dst_host = packet.payload[2]
            self.send_packet(forward_packet)
        elif packet.payload is not None and packet.payload[0] == Command.NO_REMAIN:
            self.remaining_nonanswered -= 1
            if self.remaining_nonanswered == 0:
                #print(f'For {self}, the turn is over!')
                end_turn_packet = Packet.generate_packet(-1, 0)
                end_turn_packet.src_net = self.net_info.net_addr
                end_turn_packet.payload = (Command.NO_REMAIN, None, None)
                self.receive_packet(end_turn_packet)
        elif packet.payload is not None and packet.payload[0] == Command.END_GAME:
            self.dead_characters += 1
            if self.dead_characters == len(self.ports):
                print('AAAAAAA')
                end_game_packet = Packet.generate_packet(-1, 0)
                end_game_packet.src_net = self.net_info.net_addr
                end_game_packet.payload = (Command.END_GAME, None, None)
                self.receive_packet(end_game_packet)
        else:
            raise ValueError(f'Switch {self} received a packet addressed to it, but for what reason, it does not know')

    def send_packet(self, packet: Packet):
        self.dead_characters = 0
        if packet.dst_host == Target.BROADCAST:
            if packet.payload is None or packet.payload[0] != Command.END_TURN:
                self.remaining_nonanswered += len(self.ports)
            for host in self.ports:
                host.send_packet(packet, sender=self)
        elif packet.dst_host == Target.RANDOM_UNICAST:
            host_ID = random.randint(0, len(self.ports) - 1)
            self.remaining_nonanswered += 1
            self.ports[host_ID].send_packet(packet, sender=self)
        elif packet.dst_host == Target.SELF_UNICAST:
            self.process_packet(packet)
        elif packet.dst_host == Target.PLAYER_UNICAST:
            self.packet_queue.append(packet)

            query_packet = Packet(id=None, src_net=self.net_info.net_addr, dst_net=0,
                                  dst_host=packet.src_net, payload=(Command.QUERY, Variable.CHARACTER, 'Input target ID: '))
            self.router.send_packet(query_packet, sender=self)
        elif packet.dst_host == Target.TARGET_UNICAST:
            raise ValueError('Switch received packet destined to a specific host, without the host address')
        else:
            success = False
            for host in self.ports:
                if host.address.host_addr == packet.dst_host:
                    if success:
                        raise ConnectionError(f'Two hosts with the same address connected to switch {self}')
                    else:
                        self.remaining_nonanswered += 1
                        host.send_packet(packet, sender=self)
                        success = True
            if not success:
                raise ConnectionError(f'Packet {packet} could not be delivered, because the destination host is not connected to switch {self}')

    def receive_packet(self, packet: Packet):
        if packet.dst_net == self.net_info.net_addr:
            if packet.dst_host == self.net_info.host_addr:
                self.process_packet(packet)
            else:
                self.send_packet(packet)
        else:
            self.router.send_packet(packet, sender=self)
