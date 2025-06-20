from abc import abstractmethod, ABCMeta
from src.backend.Packet import Packet

class PacketProcessor(metaclass=ABCMeta):
    @abstractmethod
    def process_packet(self, packet: Packet):
        pass

