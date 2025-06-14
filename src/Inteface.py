from abc import abstractclassmethod
from Packet import Packet
from Connection import Connection

class Interface:
    def __init__(self, net_addr: int, host_addr: int, connection: Connection) -> None:
        self.net_addr = net_addr
        self.host_addr = host_addr
        self.connection = connection

    @abstractclassmethod
    def receive_packet(self, packet: Packet) -> None:
        pass

    def send_packet(self, packet: Packet, sender=None) -> None:
        self.connection.transfer_packet(sender, packet)
