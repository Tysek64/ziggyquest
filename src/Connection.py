from Packet import Packet

class Connection:
    def __init__(self, begin, end) -> None:
        self.begin = begin
        self.end = end

    def transfer_packet(self, sender, packet: Packet) -> None:
        if sender is self.begin:
            print(f'{self.begin} -> {self.end}')
            self.end.receive_packet(packet)
        elif sender is self.end:
            print(f'{self.end} -> {self.begin}')
            self.begin.receive_packet(packet)
        else:
            raise ConnectionError('The sender is not connected to this Connection')
