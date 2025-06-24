from dataclasses import dataclass
from src.backend.PacketEnums import Target, Command, Variable, Value, Team, str_to_enum, enum_to_str

@dataclass
class Packet:
    id: int
    src_net: int
    dst_net: int
    dst_host: Target | int
    payload: (Command, Variable, Value | int)

    @staticmethod
    def make_packet(template: tuple = (None, None, None, None, None)):
        return Packet(id=None, src_net=None, dst_net=template[0], dst_host=template[1], payload=(template[2], template[3], template[4]))

    @staticmethod
    def generate_packet(net_addr: int, host_addr: int):
        return Packet(src_net=None, dst_net=net_addr, dst_host=host_addr, payload=None, id=None)

    def serialize(self):
        packet = {
                'id': self.id,
                'src_net': self.src_net,
                'dst_net': self.dst_net,
                'dst_host': self.dst_host,
                'payload': self.payload
        }

        try:
            packet['dst_net'] = enum_to_str[packet['dst_net']]
        except: pass

        try:
            packet['dst_host'] = enum_to_str[packet['dst_host']]
        except: pass

        if self.payload is not None:
            try:
                packet['payload'] = (enum_to_str[packet['payload'][0]], packet['payload'][1], packet['payload'][2])
            except: pass

            try:
                packet['payload'] = (packet['payload'][0], enum_to_str[packet['payload'][1]], packet['payload'][2])
            except: pass

            try:
                packet['payload'] = (packet['payload'][0], packet['payload'][1], enum_to_str[packet['payload'][2]])
            except: pass

        return packet

    @staticmethod
    def deserialize(packet: dict):
        try:
            packet['dst_net'] = str_to_enum[packet['dst_net']]
        except: pass

        try:
            packet['dst_host'] = str_to_enum[packet['dst_host']]
        except: pass

        if packet['payload'] is not None:
            try:
                packet['payload'] = (str_to_enum[packet['payload'][0]], packet['payload'][1], packet['payload'][2])
            except: pass

            try:
                packet['payload'] = (packet['payload'][0], str_to_enum[packet['payload'][1]], packet['payload'][2])
            except: pass

            try:
                packet['payload'] = (packet['payload'][0], packet['payload'][1], str_to_enum[packet['payload'][2]])
            except: pass

        return Packet(packet['id'], packet['src_net'], packet['dst_net'], packet['dst_host'], packet['payload'])
