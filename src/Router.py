from Packet import Packet
from Connection import Connection
from Inteface import Interface
from NetDevice import NetDevice

class Router(NetDevice):
    def __init__(self, hostname: str | None = None):
        self.ports: list[Interface] = []
        self.hostname = hostname

    def __str__(self):
        return self.hostname if self.hostname is not None else super.__str__(self)

    def add_interface(self, interface: Interface):
        self.ports.append(interface)

    def send_packet(self, packet):
        pass

    def receive_packet(self, packet: Packet):
        success = False
        for port in self.ports:
            if port.address.net_addr == packet.dst_net:
                if success:
                    raise ConnectionError(f'Two networks with the same address connected to router {self}')
                else:
                    port.send_packet(packet, sender=self)
                    success = True
        if not success:
            raise ConnectionError(f'Packet {packet} could not be routed, because the destination network is not connected to router {self}')
