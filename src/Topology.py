from Host import Host
from Switch import Switch
from Router import Router
from Connection import Connection
from Inteface import Interface
from PacketEnums import Target

if __name__ == '__main__':
    mainRouter = Router('net0.router')

    sw1 = Switch(1, 'net1.switch')
    sw2 = Switch(2, 'net2.switch')

    h11 = Host('net1.host1')
    h12 = Host('net1.host2')
    h21 = Host('net2.host1')
    h22 = Host('net2.host2')

    rs1con = Connection(mainRouter, sw1)
    rs2con = Connection(mainRouter, sw2)

    h1s1con = Connection(sw1, h11)
    h2s1con = Connection(sw1, h12)
    h1s2con = Connection(sw2, h21)
    h2s2con = Connection(sw2, h22)

    mainRouter.add_interface(Interface(1, 0, rs1con))
    mainRouter.add_interface(Interface(2, 0, rs2con))

    sw1.connect_router(Interface(0, 0, rs1con))
    sw2.connect_router(Interface(0, 0, rs2con))

    sw1.add_interface(Interface(1, 1, h1s1con))
    sw1.add_interface(Interface(1, 2, h2s1con))
    sw2.add_interface(Interface(2, 1, h1s2con))
    sw2.add_interface(Interface(2, 2, h2s2con))

    h11.connect_interface(Interface(1, 0, h1s1con))
    h12.connect_interface(Interface(1, 0, h2s1con))
    h21.connect_interface(Interface(2, 0, h1s2con))
    h22.connect_interface(Interface(2, 0, h2s2con))

    print('=== UNICAST TEST ===')
    packet = h11.generate_packet(2, 2)
    h11.send_packet(packet)

    print('\n=== ROUTED BROADCAST TEST ===')
    packet = h12.generate_packet(2, Target.BROADCAST)
    h12.send_packet(packet)

    print('\n=== SELF BROADCAST TEST ===')
    packet = h12.generate_packet(1, Target.BROADCAST)
    h12.send_packet(packet)

    print('\n=== RANDOM UNICAST TEST ===')
    packet = h11.generate_packet(2, Target.RANDOM_UNICAST)
    h11.send_packet(packet)
    packet = h22.generate_packet(2, Target.RANDOM_UNICAST)
    h22.send_packet(packet)

