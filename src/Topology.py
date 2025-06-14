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
    sw0 = Switch(0, 'net0.switch')

    h11 = Host('net1.host1')
    h12 = Host('net1.host2')
    h21 = Host('net2.host1')
    h22 = Host('net2.host2')

    p1 = Host('net0.player1')
    p2 = Host('net0.player2')

    rs1con = Connection(mainRouter, sw1)
    rs2con = Connection(mainRouter, sw2)
    rs0con = Connection(mainRouter, sw0)

    h1s1con = Connection(sw1, h11)
    h2s1con = Connection(sw1, h12)
    h1s2con = Connection(sw2, h21)
    h2s2con = Connection(sw2, h22)

    p1s0con = Connection(sw0, p1)
    p2s0con = Connection(sw0, p2)

    mainRouter.add_interface(Interface(1, 0, rs1con))
    mainRouter.add_interface(Interface(2, 0, rs2con))
    mainRouter.add_interface(Interface(0, 0, rs0con))

    sw1.connect_router(Interface(0, 0, rs1con))
    sw2.connect_router(Interface(0, 0, rs2con))
    sw0.connect_router(Interface(0, 0, rs0con))

    sw1.add_interface(Interface(1, 1, h1s1con))
    sw1.add_interface(Interface(1, 2, h2s1con))
    sw2.add_interface(Interface(2, 1, h1s2con))
    sw2.add_interface(Interface(2, 2, h2s2con))
    sw0.add_interface(Interface(0, 1, p1s0con))
    sw0.add_interface(Interface(0, 2, p2s0con))

    h11.connect_interface(Interface(1, 0, h1s1con))
    h12.connect_interface(Interface(1, 0, h2s1con))
    h21.connect_interface(Interface(2, 0, h1s2con))
    h22.connect_interface(Interface(2, 0, h2s2con))

    p1.connect_interface(Interface(0, 0, p1s0con))
    p2.connect_interface(Interface(0, 0, p2s0con))

    print('=== ROUTED TARGET UNICAST TEST ===')
    packet = h11.generate_packet(2, 2)
    h11.send_packet(packet)

    print('\n=== SELF TARGET UNICAST TEST ===')
    packet = h11.generate_packet(1, 2)
    h11.send_packet(packet)

    print('\n=== ROUTED SELF UNICAST TEST ===')
    packet = h11.generate_packet(2, Target.SELF_UNICAST)
    h11.send_packet(packet)

    print('\n=== SELF SELF UNICAST TEST ===')
    packet = h11.generate_packet(1, Target.SELF_UNICAST)
    h11.send_packet(packet)

    print('\n=== ROUTED BROADCAST TEST ===')
    packet = h12.generate_packet(2, Target.BROADCAST)
    h12.send_packet(packet)

    print('\n=== SELF BROADCAST TEST ===')
    packet = h12.generate_packet(1, Target.BROADCAST)
    h12.send_packet(packet)

    print('\n=== ROUTED RANDOM UNICAST TEST ===')
    packet = h11.generate_packet(2, Target.RANDOM_UNICAST)
    h11.send_packet(packet)

    print('\n=== SELF RANDOM UNICAST TEST ===')
    packet = h22.generate_packet(2, Target.RANDOM_UNICAST)
    h22.send_packet(packet)

    print('\n=== ROUTED PLAYER UNICAST TEST ===')
    packet = h11.generate_packet(2, Target.PLAYER_UNICAST)
    h11.send_packet(packet)

    print('\n=== SELF PLAYER UNICAST TEST ===')
    packet = h21.generate_packet(2, Target.PLAYER_UNICAST)
    h21.send_packet(packet)
