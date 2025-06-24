from src.backend.processors.PacketProcessor import PacketProcessor
from src.backend.Packet import Packet
from src.backend.PacketEnums import Command

class PlayerProcessor(PacketProcessor):
    def process_packet(self, packet: Packet) -> list[Packet]:
        if packet.payload is not None and packet.payload[0] == Command.QUERY:
            reply_packet = Packet(id=None, src_net=None, dst_net=packet.src_net, dst_host=0, payload=None)
            reply_packet.payload = (Command.REPLY, None, int(input(packet.payload[2]).strip()))

            return [reply_packet]
        elif packet.payload is not None and packet.payload[0] == Command.REPLY:
            print(packet.payload[2])
        return []
            
