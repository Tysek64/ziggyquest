from abc import ABCMeta, abstractmethod
from src.backend.NetInfo import NetInfo
from src.backend.net_devices.Inteface import Interface
from src.backend.Packet import Packet
from src.backend.net_devices.NetDevice import NetDevice

class BaseRouter(NetDevice, metaclass=ABCMeta):
    def __init__(self, net_info: NetInfo, hostname: str | None = None):
        self.ports: list[Interface] = []
        self.net_info = net_info
        self.hostname = hostname
        self.finished_turn = []
        self.current_team = 1

    def __str__(self):
        return self.hostname if self.hostname is not None else super.__str__(self)

    def add_interface(self, interface: Interface):
        self.ports.append(interface)
        self.finished_turn.append(True)

    @abstractmethod
    def end_turn(self):
        pass

    @abstractmethod
    def process_packet(self, packet: Packet):
        pass

    @abstractmethod
    def handshake(self):
        pass

    def send_packet(self, packet: Packet):
        packet.src_net = self.net_info.net_addr
        self.receive_packet(packet)

    def receive_packet(self, packet: Packet):
        success = False
        for port in self.ports:
            if port.address.net_addr == packet.dst_net:
                if success:
                    raise ConnectionError(f'Two networks with the same address connected to router {self}')
                else:
                    self.finished_turn[port.address.net_addr] = False
                    port.send_packet(packet, sender=self)
                    success = True
        if not success:
            self.process_packet(packet)