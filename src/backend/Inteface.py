from src.backend.Packet import Packet
from src.backend.Connection import Connection
from src.backend.NetInfo import NetInfo

class Interface:
    def __init__(self, address: NetInfo, connection: Connection) -> None:
        self.address = address
        self.connection = connection

    def send_packet(self, packet: Packet, sender=None) -> None:
        self.connection.transfer_packet(sender, packet)
