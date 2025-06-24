from src.backend.net_devices.Switch import Switch
from src.backend.net_devices.BattleRouter import BattleRouter
from src.backend.net_devices.Host import Host
from src.backend.NetInfo import NetInfo
from src.backend.net_devices.Inteface import Interface
from src.backend.net_devices.Connection import Connection

class Battle:
    def __init__(self, router = BattleRouter(net_info=NetInfo(net_addr=-1, host_addr=0), hostname='router')):
        self.mainRouter = router

        self.connections = {}
        self.switches = {}
        self.hosts = {}

    def add_switch(self, switch: Switch):
        if switch.net_info.net_addr in self.switches.keys():
            raise ValueError('This subnet already has a switch connected!')

        self.switches[switch.net_info.net_addr] = switch
        self.connections[(switch.net_info.net_addr, self.mainRouter.net_info)] = Connection(self.mainRouter, switch)

        self.mainRouter.add_interface(Interface(switch.net_info, self.connections[(switch.net_info.net_addr, self.mainRouter.net_info)]))
        self.switches[switch.net_info.net_addr].connect_router(Interface(self.mainRouter.net_info, self.connections[(switch.net_info.net_addr, self.mainRouter.net_info)]))

    def add_host(self, host: Host):
        if host.net_info.net_addr not in self.switches.keys():
            raise ValueError('The host\'s subnet is not connected to the network!')

        if host.net_info in self.hosts.keys():
            raise ValueError('A host with the same network address is already present!')

        self.hosts[host.net_info] = host
        self.connections[(host.net_info.net_addr, host.net_info)] = Connection(self.switches[host.net_info.net_addr], host)

        self.switches[host.net_info.net_addr].add_interface(Interface(host.net_info, self.connections[(host.net_info.net_addr, host.net_info)]))
        self.hosts[host.net_info].connect_interface(Interface(self.switches[host.net_info.net_addr].net_info, self.connections[(host.net_info.net_addr, host.net_info)]))

    def print_status(self):
        print(self.mainRouter)
        print()
        for k, v in self.switches.items():
            print(k, v, sep=': ')
        print()
        for k, v in self.hosts.items():
            print(k, v, sep=': ')
        print()
        for k, v in self.connections.items():
            print(k, v, sep=': ')
