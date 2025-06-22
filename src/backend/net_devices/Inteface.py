from src.backend.Packet import Packet
from src.backend.net_devices.Connection import Connection
from src.backend.NetInfo import NetInfo

class Interface:
    def __init__(self, address: NetInfo, connection: Connection) -> None:
        self.address = address
        self.connection = connection

    def send_packet(self, packet: Packet, sender=None) -> None:
        self.connection.transfer_packet(sender, packet)
