from dataclasses import dataclass
from PacketEnums import Target, Command, Variable, Value, Team



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


