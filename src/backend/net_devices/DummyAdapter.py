from src.backend.net_devices.Inteface import Interface
from src.backend.net_devices.NetDevice import NetDevice
from src.backend.NetInfo import NetInfo
from src.backend.Packet import Packet
from src.backend.PacketEnums import Command, Target, Team

class DummyAdapter(NetDevice):
    def __init__(self, net_info: NetInfo, hostname = None):
        self.port: Interface = None
        self.net_info = net_info
        self.hostname = hostname

        self.queue = []

    def __str__(self):
        return self.hostname if self.hostname is not None else super.__str__(self)

    def connect_interface(self, interface: Interface):
        self.port = interface

    def send_packet(self, packet: Packet):
        self.port.send_packet(packet, sender=self)

    def receive_packet(self, packet: Packet):
        self.queue.append(packet)

    def retrieve_packets(self):
        result = self.queue
        self.queue = []
        return result
