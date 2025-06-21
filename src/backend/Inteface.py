from abc import abstractclassmethod
from src.Packet import Packet
from src.Connection import Connection
from src.NetInfo import NetInfo

class Interface:
    def __init__(self, address: NetInfo, connection: Connection) -> None:
        self.address = address
        self.connection = connection

    def send_packet(self, packet: Packet, sender=None) -> None:
        self.connection.transfer_packet(sender, packet)
