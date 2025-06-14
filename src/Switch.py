from Connection import Connection
from Inteface import Interface
from Packet import Packet
from PacketEnums import Target
import random

class Switch:
    def __init__(self, net_addr: int, hostname=None):
        self.net_addr = net_addr
        self.ports: list[Interface] = []
        self.router: Interface = None

        self.hostname = hostname

    def __str__(self):
        return self.hostname if self.hostname is not None else super.__str__(self)

    def add_interface(self, interface: Interface):
        self.ports.append(interface)

    def connect_router(self, interface: Interface):
        self.router = interface

    def send_packet(self, packet: Packet):
        if packet.dst_host == Target.BROADCAST:
            for host in self.ports:
                host.send_packet(packet, sender=self)
        elif packet.dst_host == Target.RANDOM_UNICAST:
            self.ports[random.randint(0, len(self.ports) - 1)].send_packet(packet, sender=self)
        elif packet.dst_host == Target.SELF_UNICAST:
            pass
        elif packet.dst_host == Target.PLAYER_UNICAST:
            pass 
        elif packet.dst_host == Target.TARGET_UNICAST:
            pass
        else:
            for host in self.ports:
                if host.host_addr == packet.dst_host:
                    host.send_packet(packet, sender=self)

    def receive_packet(self, packet: Packet):
        if packet.dst_net == self.net_addr:
            self.send_packet(packet)
        else:
            self.router.send_packet(packet, sender=self)
