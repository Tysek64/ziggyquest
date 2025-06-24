from dataclasses import dataclass

@dataclass(unsafe_hash=True)
class NetInfo:
    net_addr: int
    host_addr: int
