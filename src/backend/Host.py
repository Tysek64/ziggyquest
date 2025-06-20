from src.backend.Inteface import Interface
from src.backend.Packet import Packet
from src.backend.PacketEnums import Command, Target, Team
from src.backend.NetDevice import NetDevice
from src.backend.NetInfo import NetInfo
from src.backend.PacketProcessor import PacketProcessor

class Host(NetDevice):
    def __init__(self, net_info: NetInfo, hostname = None, processor: PacketProcessor = None):
        self.port: Interface = None
        self.net_info = net_info
        self.hostname = hostname
        self.packet_processor = processor

    def __str__(self):
        return self.hostname if self.hostname is not None else super.__str__(self)

    def connect_interface(self, interface: Interface):
        self.port = interface

    def generate_packet(self, net_addr: int, host_addr: int) -> Packet:
        return Packet(src_net=self.port.address.net_addr, dst_net=net_addr, dst_host=host_addr, payload=None, id=None)

    def send_packet(self, packet: Packet):
        packet.src_net = self.net_info.net_addr
        if packet.dst_host == Target.SELF_UNICAST:
            packet.dst_host = self.net_info.host_addr

        if packet.dst_net == Team.ME:
            packet.dst_net = self.net_info.net_addr
        elif packet.dst_net == Team.OPPONENT:
            packet.dst_net = 3 - self.net_info.net_addr # zalozenie - dwoch graczy

        self.port.send_packet(packet, sender=self)

    def receive_packet(self, packet: Packet):
        if packet.payload is not None and packet.payload[0] in (Command.SET, Command.INCREASE, Command.DECREASE):
            print(f'{self} received {packet}')
        reply_packets = self.packet_processor.process_packet(packet)
        end_turn_packet = Packet.generate_packet(self.port.address.net_addr, self.port.address.host_addr)
        end_turn_packet.payload = (Command.NO_REMAIN, None, None)
        reply_packets.append(end_turn_packet)
        if packet.payload is None or packet.payload[0] != Command.END_TURN:
            for reply_packet in reply_packets:
                self.send_packet(reply_packet)
