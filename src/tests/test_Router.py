import pytest
from src.backend.net_devices.BattleRouter import BattleRouter
from src.backend.net_devices.SelectionRouter import SelectionRouter
from src.backend.net_devices.DummyAdapter import DummyAdapter
from src.backend.net_devices.Connection import Connection
from src.backend.net_devices.Inteface import Interface
from src.backend.NetInfo import NetInfo
from src.backend.Packet import Packet

@pytest.mark.parametrize('router, packet', [
                         (BattleRouter(NetInfo(-1, 0)), Packet(id=None, src_net=0, dst_net=0, dst_host=0, payload=None)),
                         (BattleRouter(NetInfo(-1, 0)), Packet(id=None, src_net=0, dst_net=1, dst_host=0, payload=None)),
                         (BattleRouter(NetInfo(-1, 0)), Packet(id=None, src_net=0, dst_net=2, dst_host=0, payload=None)),
                         (SelectionRouter(NetInfo(-1, 0)), Packet(id=None, src_net=0, dst_net=0, dst_host=0, payload=None)),
                         (SelectionRouter(NetInfo(-1, 0)), Packet(id=None, src_net=0, dst_net=1, dst_host=0, payload=None)),
                         (SelectionRouter(NetInfo(-1, 0)), Packet(id=None, src_net=0, dst_net=2, dst_host=0, payload=None)),
    ])
def test_correct (router, packet):
    dummies = [
        DummyAdapter(NetInfo(0, 0)),
        DummyAdapter(NetInfo(1, 0)),
        DummyAdapter(NetInfo(2, 0))
    ]

    con0 = Connection(router, dummies[0])
    con1 = Connection(router, dummies[1])
    con2 = Connection(router, dummies[2])

    router.add_interface(Interface(NetInfo(0, 0), con0))
    router.add_interface(Interface(NetInfo(1, 0), con1))
    router.add_interface(Interface(NetInfo(2, 0), con2))

    dummies[0].connect_interface(Interface(NetInfo(-1, 0), con0))
    dummies[1].connect_interface(Interface(NetInfo(-1, 0), con1))
    dummies[2].connect_interface(Interface(NetInfo(-1, 0), con2))

    dummies[0].send_packet(packet)
    assert dummies[packet.dst_net].retrieve_packets()[0] is packet

@pytest.mark.parametrize('router, packet', [
                         (BattleRouter(NetInfo(-1, 0)), Packet(id=None, src_net=0, dst_net=0, dst_host=0, payload=None)),
                         (BattleRouter(NetInfo(-1, 0)), Packet(id=None, src_net=0, dst_net=1, dst_host=0, payload=None)),
                         (BattleRouter(NetInfo(-1, 0)), Packet(id=None, src_net=0, dst_net=2, dst_host=0, payload=None)),
                         (SelectionRouter(NetInfo(-1, 0)), Packet(id=None, src_net=0, dst_net=0, dst_host=0, payload=None)),
                         (SelectionRouter(NetInfo(-1, 0)), Packet(id=None, src_net=0, dst_net=1, dst_host=0, payload=None)),
                         (SelectionRouter(NetInfo(-1, 0)), Packet(id=None, src_net=0, dst_net=2, dst_host=0, payload=None)),
    ])
def test_missing (router, packet):
    dummies = [
        DummyAdapter(NetInfo(0, 0)),
        DummyAdapter(NetInfo(1, 0))
    ]

    con0 = Connection(router, dummies[0])
    con1 = Connection(router, dummies[1])

    router.add_interface(Interface(NetInfo(0, 0), con0))
    router.add_interface(Interface(NetInfo(1, 0), con1))

    dummies[0].connect_interface(Interface(NetInfo(-1, 0), con0))
    dummies[1].connect_interface(Interface(NetInfo(-1, 0), con1))

    if packet.dst_net < len(dummies):
        dummies[0].send_packet(packet)
        assert dummies[packet.dst_net].retrieve_packets()[0] is packet
    else:
        with pytest.raises(ValueError):
            dummies[0].send_packet(packet)

@pytest.mark.parametrize('router, packet', [
                         (BattleRouter(NetInfo(-1, 0)), Packet(id=None, src_net=0, dst_net=0, dst_host=0, payload=None)),
                         (BattleRouter(NetInfo(-1, 0)), Packet(id=None, src_net=0, dst_net=1, dst_host=0, payload=None)),
                         (BattleRouter(NetInfo(-1, 0)), Packet(id=None, src_net=0, dst_net=2, dst_host=0, payload=None)),
                         (SelectionRouter(NetInfo(-1, 0)), Packet(id=None, src_net=0, dst_net=0, dst_host=0, payload=None)),
                         (SelectionRouter(NetInfo(-1, 0)), Packet(id=None, src_net=0, dst_net=1, dst_host=0, payload=None)),
                         (SelectionRouter(NetInfo(-1, 0)), Packet(id=None, src_net=0, dst_net=2, dst_host=0, payload=None)),
    ])
def test_too_many (router, packet):
    dummies = [
        DummyAdapter(NetInfo(0, 0)),
        DummyAdapter(NetInfo(1, 0)),
        DummyAdapter(NetInfo(2, 0))
    ]

    con0 = Connection(router, dummies[0])
    con1 = Connection(router, dummies[1])
    con2 = Connection(router, dummies[2])

    router.add_interface(Interface(NetInfo(0, 0), con0))
    router.add_interface(Interface(NetInfo(1, 0), con1))
    router.add_interface(Interface(NetInfo(2, 0), con2))
    router.add_interface(Interface(NetInfo(2, 0), con2))

    dummies[0].connect_interface(Interface(NetInfo(-1, 0), con0))
    dummies[1].connect_interface(Interface(NetInfo(-1, 0), con1))
    dummies[2].connect_interface(Interface(NetInfo(-1, 0), con2))

    if packet.dst_net != 2:
        dummies[0].send_packet(packet)
        assert dummies[packet.dst_net].retrieve_packets()[0] is packet
    else:
        with pytest.raises(ConnectionError):
            dummies[0].send_packet(packet)
