from dataclasses import dataclass
from PacketEnums import Target, Command, Variable, Value

@dataclass
class Packet:
    id: int
    src_net: int
    dst_net: int
    dst_host: Target | int
    payload: (Command, Variable, Value | int)

