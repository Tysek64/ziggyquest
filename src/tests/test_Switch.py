import pytest
from src.backend.net_devices.Switch import Switch
from src.backend.net_devices.DummyAdapter import DummyAdapter
from src.backend.net_devices.Connection import Connection
from src.backend.net_devices.Inteface import Interface
from src.backend.NetInfo import NetInfo
from src.backend.Packet import Packet
from src.backend.PacketEnums import Target, Command, Variable

@pytest.mark.parametrize('packet', [
                         (Packet(id=None, src_net=0, dst_net=0, dst_host=1, payload=None)),
                         (Packet(id=None, src_net=0, dst_net=0, dst_host=2, payload=None)),
                         (Packet(id=None, src_net=0, dst_net=-1, dst_host=0, payload=None)),
    ])
def test_correct (packet):
    switch = Switch(NetInfo(0, 0))
    dummies = [
        DummyAdapter(NetInfo(0, 1)),
        DummyAdapter(NetInfo(0, 2)),
    ]
    router = DummyAdapter(NetInfo(-1, 0))

    con0 = Connection(switch, dummies[0])
    con1 = Connection(switch, dummies[1])
    con2 = Connection(switch, router)

    switch.add_interface(Interface(NetInfo(0, 1), con0))
    switch.add_interface(Interface(NetInfo(0, 2), con1))
    switch.connect_router(Interface(NetInfo(-1, 0), con2))

    dummies[0].connect_interface(Interface(NetInfo(0, 0), con0))
    dummies[1].connect_interface(Interface(NetInfo(0, 0), con1))
    router.connect_interface(Interface(NetInfo(0, 0), con2))

    dummies[0].send_packet(packet)
    if packet.dst_net == 0:
        assert dummies[packet.dst_host - 1].retrieve_packets()[0] is packet
    else:
        assert router.retrieve_packets()[0] is packet

@pytest.mark.parametrize('packet', [
                         (Packet(id=None, src_net=0, dst_net=0, dst_host=1, payload=None)),
                         (Packet(id=None, src_net=0, dst_net=0, dst_host=2, payload=None)),
                         (Packet(id=None, src_net=0, dst_net=-1, dst_host=0, payload=None)),
    ])
def test_missing (packet):
    switch = Switch(NetInfo(0, 0))
    dummies = [
        DummyAdapter(NetInfo(0, 1)),
    ]
    router = DummyAdapter(NetInfo(-1, 0))

    con0 = Connection(switch, dummies[0])
    con2 = Connection(switch, router)

    switch.add_interface(Interface(NetInfo(0, 1), con0))
    switch.connect_router(Interface(NetInfo(-1, 0), con2))

    dummies[0].connect_interface(Interface(NetInfo(0, 0), con0))
    router.connect_interface(Interface(NetInfo(0, 0), con2))

    if packet.dst_host > len(dummies):
        with pytest.raises(ConnectionError):
            dummies[0].send_packet(packet)
    else:
        dummies[0].send_packet(packet)
        if packet.dst_net == 0:
            assert dummies[packet.dst_host - 1].retrieve_packets()[0] is packet
        else:
            assert router.retrieve_packets()[0] is packet

@pytest.mark.parametrize('packet', [
                         (Packet(id=None, src_net=0, dst_net=0, dst_host=1, payload=None)),
                         (Packet(id=None, src_net=0, dst_net=0, dst_host=2, payload=None)),
                         (Packet(id=None, src_net=0, dst_net=-1, dst_host=0, payload=None)),
    ])
def test_too_many (packet):
    switch = Switch(NetInfo(0, 0))
    dummies = [
        DummyAdapter(NetInfo(0, 1)),
        DummyAdapter(NetInfo(0, 2)),
    ]
    router = DummyAdapter(NetInfo(-1, 0))

    con0 = Connection(switch, dummies[0])
    con1 = Connection(switch, dummies[1])
    con2 = Connection(switch, router)

    switch.add_interface(Interface(NetInfo(0, 1), con0))
    switch.add_interface(Interface(NetInfo(0, 2), con1))
    switch.add_interface(Interface(NetInfo(0, 2), con1))
    switch.connect_router(Interface(NetInfo(-1, 0), con2))

    dummies[0].connect_interface(Interface(NetInfo(0, 0), con0))
    dummies[1].connect_interface(Interface(NetInfo(0, 0), con1))
    router.connect_interface(Interface(NetInfo(0, 0), con2))

    if packet.dst_host == 2:
        with pytest.raises(ConnectionError):
            dummies[0].send_packet(packet)
    else:
        dummies[0].send_packet(packet)
        if packet.dst_net == 0:
            assert dummies[packet.dst_host - 1].retrieve_packets()[0] is packet
        else:
            assert router.retrieve_packets()[0] is packet

@pytest.mark.parametrize('packet', [
                         (Packet(id=None, src_net=0, dst_net=0, dst_host=Target.BROADCAST, payload=None)),
                         (Packet(id=None, src_net=0, dst_net=-1, dst_host=Target.BROADCAST, payload=None)),
    ])
def test_broadcast (packet):
    switch = Switch(NetInfo(0, 0))
    dummies = [
        DummyAdapter(NetInfo(0, 1)),
        DummyAdapter(NetInfo(0, 2)),
    ]
    router = DummyAdapter(NetInfo(-1, 0))

    con0 = Connection(switch, dummies[0])
    con1 = Connection(switch, dummies[1])
    con2 = Connection(switch, router)

    switch.add_interface(Interface(NetInfo(0, 1), con0))
    switch.add_interface(Interface(NetInfo(0, 2), con1))
    switch.connect_router(Interface(NetInfo(-1, 0), con2))

    dummies[0].connect_interface(Interface(NetInfo(0, 0), con0))
    dummies[1].connect_interface(Interface(NetInfo(0, 0), con1))
    router.connect_interface(Interface(NetInfo(0, 0), con2))

    dummies[0].send_packet(packet)
    if packet.dst_net == 0:
        for dummy in dummies:
            assert dummy.retrieve_packets()[0] is packet
    else:
        assert router.retrieve_packets()[0] is packet

@pytest.mark.parametrize('packet', [
                         (Packet(id=None, src_net=0, dst_net=0, dst_host=Target.TARGET_UNICAST, payload=None)),
                         (Packet(id=None, src_net=0, dst_net=-1, dst_host=Target.TARGET_UNICAST, payload=None)),
    ])
def test_target (packet):
    switch = Switch(NetInfo(0, 0))
    dummies = [
        DummyAdapter(NetInfo(0, 1)),
        DummyAdapter(NetInfo(0, 2)),
    ]
    router = DummyAdapter(NetInfo(-1, 0))

    con0 = Connection(switch, dummies[0])
    con1 = Connection(switch, dummies[1])
    con2 = Connection(switch, router)

    switch.add_interface(Interface(NetInfo(0, 1), con0))
    switch.add_interface(Interface(NetInfo(0, 2), con1))
    switch.connect_router(Interface(NetInfo(-1, 0), con2))

    dummies[0].connect_interface(Interface(NetInfo(0, 0), con0))
    dummies[1].connect_interface(Interface(NetInfo(0, 0), con1))
    router.connect_interface(Interface(NetInfo(0, 0), con2))

    if packet.dst_net == 0:
        with pytest.raises(ValueError):
            dummies[0].send_packet(packet)
    else:
        dummies[0].send_packet(packet)
        assert router.retrieve_packets()[0] is packet

@pytest.mark.parametrize('packet', [
                         (Packet(id=None, src_net=0, dst_net=0, dst_host=Target.PLAYER_UNICAST, payload=None)),
                         (Packet(id=None, src_net=0, dst_net=-1, dst_host=Target.PLAYER_UNICAST, payload=None)),
    ])
def test_player (packet):
    switch = Switch(NetInfo(0, 0))
    dummies = [
        DummyAdapter(NetInfo(0, 1)),
        DummyAdapter(NetInfo(0, 2)),
    ]
    router = DummyAdapter(NetInfo(-1, 0))

    con0 = Connection(switch, dummies[0])
    con1 = Connection(switch, dummies[1])
    con2 = Connection(switch, router)

    switch.add_interface(Interface(NetInfo(0, 1), con0))
    switch.add_interface(Interface(NetInfo(0, 2), con1))
    switch.connect_router(Interface(NetInfo(-1, 0), con2))

    dummies[0].connect_interface(Interface(NetInfo(0, 0), con0))
    dummies[1].connect_interface(Interface(NetInfo(0, 0), con1))
    router.connect_interface(Interface(NetInfo(0, 0), con2))

    dummies[0].send_packet(packet)
    if packet.dst_net == 0:
        assert router.retrieve_packets()[0] == Packet(id=None, src_net=0, dst_net=0, dst_host=0, payload=(Command.QUERY, Variable.CHARACTER, 'Input target ID: '))
    else:
        assert router.retrieve_packets()[0] is packet

@pytest.mark.parametrize('packet', [
                         (Packet(id=None, src_net=0, dst_net=0, dst_host=Target.RANDOM_UNICAST, payload=None)),
                         (Packet(id=None, src_net=0, dst_net=-1, dst_host=Target.RANDOM_UNICAST, payload=None)),
    ])
def test_random (packet):
    switch = Switch(NetInfo(0, 0))
    dummies = [
        DummyAdapter(NetInfo(0, 1)),
        DummyAdapter(NetInfo(0, 2)),
    ]
    router = DummyAdapter(NetInfo(-1, 0))

    con0 = Connection(switch, dummies[0])
    con1 = Connection(switch, dummies[1])
    con2 = Connection(switch, router)

    switch.add_interface(Interface(NetInfo(0, 1), con0))
    switch.add_interface(Interface(NetInfo(0, 2), con1))
    switch.connect_router(Interface(NetInfo(-1, 0), con2))

    dummies[0].connect_interface(Interface(NetInfo(0, 0), con0))
    dummies[1].connect_interface(Interface(NetInfo(0, 0), con1))
    router.connect_interface(Interface(NetInfo(0, 0), con2))

    dummies[0].send_packet(packet)
    if packet.dst_net == 0:
        dum1 = dummies[0].retrieve_packets()
        dum2 = dummies[1].retrieve_packets()
        assert (len(dum1) > 0 and dum1[0] is packet) or (len(dum2) > 0 and dum2[0] is packet)
    else:
        assert router.retrieve_packets()[0] is packet

