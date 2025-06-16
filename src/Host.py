from Connection import Connection
from Inteface import Interface
from Packet import Packet
from PacketEnums import Command, Target, Team
from NetDevice import NetDevice
from NetInfo import NetInfo
# TODO host jako kontroler postaci,
class Host(NetDevice):
    def __init__(self, net_info: NetInfo, hostname = None):
        self.port: Interface = None
        self.net_info = net_info
        self.hostname = hostname

    def __str__(self):
        return self.hostname if self.hostname is not None else super.__str__(self)

    def connect_interface(self, interface: Interface):
        self.port = interface

    def generate_packet(self, net_addr: int, host_addr: int) -> Packet:
        return Packet(src_net=self.port.address.net_addr, dst_net=net_addr, dst_host=host_addr, payload=None, id=None)

    def send_packet(self, packet: Packet):
        if packet.dst_host == Target.SELF_UNICAST:
            self.receive_packet(packet)
        else:
            if packet.dst_net == Team.ME:
                packet.dst_net = self.net_info.net_addr
            elif packet.dst_net == Team.OPPONENT:
                packet.dst_net = 3 - self.net_info.net_addr # zalozenie - dwoch graczy

            self.port.send_packet(packet, sender=self)

    def receive_packet(self, packet: Packet):
        print(f'{self} received {packet}')
        if packet.payload is not None and packet.payload[0] == Command.QUERY:
            reply_packet = self.generate_packet(packet.src_net, 0)
            reply_packet.payload = (Command.REPLY, None, int(input(packet.payload[2])))

            self.send_packet(reply_packet)
