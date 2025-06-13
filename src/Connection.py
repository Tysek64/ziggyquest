from Packet import Packet

class Connection:
    def __init__(self, begin, end) -> None:
        self.begin = begin
        self.end = end

    def transfer_packet(self, sender, packet: Packet) -> None:
        if sender is self.begin:
            self.end.receive_packet(packet)
        elif sender is self.end:
            self.begin.receive_packet(packet)
        else:
            raise ConnectionError('Object is neither a sender nor a receiver')
