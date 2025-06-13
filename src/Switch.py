from Connection import Connection
from Packet import Packet
from PacketEnums import Target
import random

class Switch:
    def __init__(self, net_addr: int):
        self.net_addr = net_addr
        self.hosts: list[Connection] = []
        self.router: Connection = Connection()

    def send_packet(self, packet: Packet):
        if packet.dst_host == Target.BROADCAST:
            for host in self.hosts:
                host.transfer_packet(self, packet)
        elif packet.dst_host == Target.RANDOM_UNICAST:
            self.hosts[random.randint(0, len(self.hosts))].transfer_packet(self, packet)
        elif packet.dst_host == Target.SELF_UNICAST:
            pass

    def receive_packet(self, packet: Packet):
        if packet.dst_net == self.net_addr:
            self.send_packet(packet)
        else:
            self.router.transfer_packet(self, packet)
