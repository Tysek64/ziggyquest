from abc import abstractclassmethod
from Packet import Packet


class Interface:
    def __init__(self, net_addr: int, host_addr: int, connection: Connection) -> None:
        pass

    @abstractclassmethod
    def receive_packet(self, packet: Packet) -> None:
        pass

    @abstractclassmethod
    def send_packet(self, packet: Packet) -> None:
        pass
