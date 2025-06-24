from src.backend.Packet import Packet
from src.backend.NetInfo import NetInfo
from src.backend.processors.PacketProcessor import PacketProcessor
from src.backend.PacketEnums import Command, Team, Target, Variable, Value
import socket
import json

class ServerSocket(PacketProcessor):
    def __init__(self, ip_addr, port=8233, encoding='utf-8'):
        self.ip_addr = ip_addr
        self.port = port
        self.encoding = encoding

        self.socket = None
        self.client = None

        self.wait_for_connection()
        self.handshake()

    def wait_for_connection(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip_addr, self.port))
        self.socket.listen(1)

        while self.client is None:
            self.client, client_address = self.socket.accept()

        print(f'Established connection with {client_address}')

    def handshake(self):
        parsed_net_info = {'net_addr': 0, 'host_addr': 1}
        self.client.sendall(json.dumps(parsed_net_info).encode(self.encoding))

    def quit(self):
        self.socket.close()

    def process_packet(self, packet: Packet):
        self.client.sendall(json.dumps(packet.serialize()).encode(self.encoding))
        received = self.client.recv(2048)
        return self.decode_packets(received)

    def decode_packets(self, repr: bytes) -> Packet:
        result = []
        parsed_json = json.loads(repr.decode(self.encoding))
        for packet in parsed_json:
            result.append(Packet.deserialize(packet))

        return result

if __name__ == '__main__':
    server = ServerSocket(NetInfo(0, 1), 'localhost', 8233)
    server.wait_for_connection()
    server.handshake()
    server.quit()
