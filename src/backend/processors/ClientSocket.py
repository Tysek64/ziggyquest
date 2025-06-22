from src.backend.NetInfo import NetInfo
from src.backend.processors.PacketProcessor import PacketProcessor
from src.backend.processors.PlayerProcessor import PlayerProcessor
from src.backend.Packet import Packet
import socket
import json

class ClientSocket(PacketProcessor):
    def __init__(self, ip_addr, port=8233, encoding='utf-8', processor=PlayerProcessor()):
        self.ip_addr = ip_addr
        self.port = port
        self.encoding = encoding

        self.socket = None

        self.processor = processor
        self.connect_to_server()
        self.handshake()

    def connect_to_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip_addr, self.port))

    def handshake(self):
        net_info = self.socket.recvfrom(1024)
        net_info_parsed = json.loads(net_info[0].decode(self.encoding))

    def receive_packet(self):
        print('a')
        packet = self.socket.recvfrom(1024)[0]
        deserialized = Packet.deserialize(json.loads(packet.decode(self.encoding)))

        result = self.process_packet(deserialized)

        self.socket.sendall(self.encode_packets(result))

    def process_packet(self, packet):
        return self.processor.process_packet(packet)
    
    def encode_packets(self, packets: list[Packet]) -> bytes:
        serialized = [packet.serialize() for packet in packets]

        return json.dumps(serialized).encode(self.encoding)

if __name__ == '__main__':
    client = ClientSocket('localhost', 8233)
    client.connect_to_server()
    client.handshake()
    while True:
        client.receive_packet()
    client.quit()
