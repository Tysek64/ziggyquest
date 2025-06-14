from Connection import Connection
from Inteface import Interface
from Packet import Packet
from PacketEnums import Target, Command
import random

class Switch:
    def __init__(self, net_addr: int, hostname=None):
        self.net_addr = net_addr
        self.ports: list[Interface] = []
        self.router: Interface = None

        self.hostname = hostname

        self.packet_queue: list[Packet] = []

    def __str__(self):
        return self.hostname if self.hostname is not None else super.__str__(self)

    def add_interface(self, interface: Interface):
        self.ports.append(interface)

    def connect_router(self, interface: Interface):
        self.router = interface

    def process_packet(self, packet: Packet):
        print(f'{self} received {packet}')
        if packet.payload is not None and packet.payload[0] == Command.REPLY:
            try:
                forward_packet = self.packet_queue.pop(0)
            except IndexError:
                raise ValueError(f'Switch {self} received a reply to no asked questions')
            forward_packet.dst_host = packet.payload[2]
            self.send_packet(forward_packet)
        else:
            raise ValueError(f'Switch {self} received a packet addressed to it, but for what reason, it does not know')

    def send_packet(self, packet: Packet):
        if packet.dst_host == Target.BROADCAST:
            for host in self.ports:
                host.send_packet(packet, sender=self)
        elif packet.dst_host == Target.RANDOM_UNICAST:
            self.ports[random.randint(0, len(self.ports) - 1)].send_packet(packet, sender=self)
        elif packet.dst_host == Target.SELF_UNICAST:
            pass
        elif packet.dst_host == Target.PLAYER_UNICAST:
            self.packet_queue.append(packet)

            query_packet = Packet(id=None, src_net=self.net_addr, dst_net=0, dst_host=packet.src_net, payload=(Command.QUERY, None, 'Input target ID: '))
            self.router.send_packet(query_packet, sender=self)
        elif packet.dst_host == Target.TARGET_UNICAST:
            raise ValueError('Switch received packet destined to a specific host, without the host address')
        else:
            success = False
            for host in self.ports:
                if host.host_addr == packet.dst_host:
                    if success:
                        raise ConnectionError(f'Two hosts with the same address connected to switch {self}')
                    else:
                        host.send_packet(packet, sender=self)
                        success = True
            if not success:
                raise ConnectionError(f'Packet {packet} could not be delivered, because the destination host is not connected to switch {self}')

    def receive_packet(self, packet: Packet):
        if packet.dst_net == self.net_addr:
            if packet.dst_host == 0:
                self.process_packet(packet)
            else:
                self.send_packet(packet)
        else:
            self.router.send_packet(packet, sender=self)
