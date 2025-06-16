from abc import abstractmethod, ABCMeta
from Packet import Packet

class NetDevice(metaclass=ABCMeta):
    @abstractmethod
    def receive_packet(self, packet: Packet):
        pass

    @abstractmethod
    def send_packet(self, packet: Packet):
        pass