from PacketProcessor import PacketProcessor
from Packet import Packet
from PacketEnums import Command

class PlayerProcessor(PacketProcessor):
    def process_packet(self, packet: Packet) -> list[Packet]:
        if packet.payload is not None and packet.payload[0] == Command.QUERY:
            reply_packet = self.generate_packet(packet.src_net, 0)
            reply_packet.payload = (Command.REPLY, None, int(input(packet.payload[2])))

            return [reply_packet]
        return []
            
