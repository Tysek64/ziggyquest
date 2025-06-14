from Connection import Connection
from Inteface import Interface
from Packet import Packet

class Host:
    def __init__(self, hostname = None):
        self.port: Interface = None
        self.hostname = hostname

    def __str__(self):
        return self.hostname if self.hostname is not None else super.__str__(self)

    def connectInterface(self, interface: Interface):
        self.port = interface

    def generatePacket(self, net_addr: int, host_addr: int) -> Packet:
        return Packet(src_net=self.port.net_addr, dst_net=net_addr, dst_host=host_addr, payload=None, id=None)

    def send_packet(self, packet: Packet):
        self.port.send_packet(packet, sender=self)

    def receive_packet(self, packet: Packet):
        print(f'Received packet {packet}')
