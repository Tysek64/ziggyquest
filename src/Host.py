from Connection import Connection
from Inteface import Interface
from Packet import Packet
from PacketEnums import Command, Target

class Host:
    def __init__(self, hostname = None):
        self.port: Interface = None
        self.hostname = hostname

    def __str__(self):
        return self.hostname if self.hostname is not None else super.__str__(self)

    def connect_interface(self, interface: Interface):
        self.port = interface

    def generate_packet(self, net_addr: int, host_addr: int) -> Packet:
        return Packet(src_net=self.port.net_addr, dst_net=net_addr, dst_host=host_addr, payload=None, id=None)

    def send_packet(self, packet: Packet):
        if packet.dst_host == Target.SELF_UNICAST:
            self.receive_packet(packet)
        else:
            self.port.send_packet(packet, sender=self)

    def receive_packet(self, packet: Packet):
        print(f'{self} received {packet}')
        if packet.payload is not None and packet.payload[0] == Command.QUERY:
            reply_packet = self.generate_packet(packet.src_net, 0)
            reply_packet.payload = (Command.REPLY, None, int(input(packet.payload[2])))

            self.send_packet(reply_packet)
