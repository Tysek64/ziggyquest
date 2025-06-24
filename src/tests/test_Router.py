import pytest
from src.backend.net_devices.BattleRouter import BattleRouter
from src.backend.net_devices.SelectionRouter import SelectionRouter
from src.backend.net_devices.DummyAdapter import DummyAdapter
from src.backend.net_devices.Connection import Connection
from src.backend.net_devices.Inteface import Interface
from src.backend.NetInfo import NetInfo
from src.backend.Packet import Packet

def test_correct ():
    router = BattleRouter(NetInfo(-1, 0))
    dummy0 = DummyAdapter(NetInfo(0, 0))
    dummy1 = DummyAdapter(NetInfo(1, 0))
    dummy2 = DummyAdapter(NetInfo(2, 0))

    con0 = Connection(router, dummy0)
    con1 = Connection(router, dummy1)
    con2 = Connection(router, dummy2)

    router.add_interface(Interface(NetInfo(0, 0), con0))
    router.add_interface(Interface(NetInfo(1, 0), con1))
    router.add_interface(Interface(NetInfo(2, 0), con2))

    dummy0.connect_interface(Interface(NetInfo(-1, 0), con0))
    dummy1.connect_interface(Interface(NetInfo(-1, 0), con1))
    dummy2.connect_interface(Interface(NetInfo(-1, 0), con2))

    packet = Packet(id=None, src_net=0, dst_net=0, dst_host=0, payload=None)
    dummy0.send_packet(packet)
    assert dummy0.retrieve_packets()[0] is packet

    packet = Packet(id=None, src_net=0, dst_net=1, dst_host=0, payload=None)
    dummy0.send_packet(packet)
    assert dummy1.retrieve_packets()[0] is packet

    packet = Packet(id=None, src_net=0, dst_net=2, dst_host=0, payload=None)
    dummy0.send_packet(packet)
    assert dummy2.retrieve_packets()[0] is packet

def test_missing ():
    router = BattleRouter(NetInfo(-1, 0))
    dummy0 = DummyAdapter(NetInfo(0, 0))
    dummy1 = DummyAdapter(NetInfo(1, 0))

    con0 = Connection(router, dummy0)
    con1 = Connection(router, dummy1)

    router.add_interface(Interface(NetInfo(0, 0), con0))
    router.add_interface(Interface(NetInfo(1, 0), con1))

    dummy0.connect_interface(Interface(NetInfo(-1, 0), con0))
    dummy1.connect_interface(Interface(NetInfo(-1, 0), con1))

    packet = Packet(id=None, src_net=0, dst_net=0, dst_host=0, payload=None)
    dummy0.send_packet(packet)
    assert dummy0.retrieve_packets()[0] is packet

    packet = Packet(id=None, src_net=0, dst_net=1, dst_host=0, payload=None)
    dummy0.send_packet(packet)
    assert dummy1.retrieve_packets()[0] is packet

    with pytest.raises(ValueError):
        packet = Packet(id=None, src_net=0, dst_net=2, dst_host=0, payload=None)
        dummy0.send_packet(packet)

def test_too_many ():
    router = BattleRouter(NetInfo(-1, 0))
    dummy0 = DummyAdapter(NetInfo(0, 0))
    dummy1 = DummyAdapter(NetInfo(1, 0))
    dummy2 = DummyAdapter(NetInfo(2, 0))

    con0 = Connection(router, dummy0)
    con1 = Connection(router, dummy1)
    con2 = Connection(router, dummy2)

    router.add_interface(Interface(NetInfo(0, 0), con0))
    router.add_interface(Interface(NetInfo(1, 0), con1))
    router.add_interface(Interface(NetInfo(2, 0), con2))
    router.add_interface(Interface(NetInfo(2, 0), con2))

    dummy0.connect_interface(Interface(NetInfo(-1, 0), con0))
    dummy1.connect_interface(Interface(NetInfo(-1, 0), con1))
    dummy2.connect_interface(Interface(NetInfo(-1, 0), con2))

    packet = Packet(id=None, src_net=0, dst_net=0, dst_host=0, payload=None)
    dummy0.send_packet(packet)
    assert dummy0.retrieve_packets()[0] is packet

    packet = Packet(id=None, src_net=0, dst_net=1, dst_host=0, payload=None)
    dummy0.send_packet(packet)
    assert dummy1.retrieve_packets()[0] is packet

    with pytest.raises(ConnectionError):
        packet = Packet(id=None, src_net=0, dst_net=2, dst_host=0, payload=None)
        dummy0.send_packet(packet)

def test_correct_2 ():
    router = SelectionRouter(NetInfo(-1, 0))
    dummy0 = DummyAdapter(NetInfo(0, 0))
    dummy1 = DummyAdapter(NetInfo(1, 0))
    dummy2 = DummyAdapter(NetInfo(2, 0))

    con0 = Connection(router, dummy0)
    con1 = Connection(router, dummy1)
    con2 = Connection(router, dummy2)

    router.add_interface(Interface(NetInfo(0, 0), con0))
    router.add_interface(Interface(NetInfo(1, 0), con1))
    router.add_interface(Interface(NetInfo(2, 0), con2))

    dummy0.connect_interface(Interface(NetInfo(-1, 0), con0))
    dummy1.connect_interface(Interface(NetInfo(-1, 0), con1))
    dummy2.connect_interface(Interface(NetInfo(-1, 0), con2))

    packet = Packet(id=None, src_net=0, dst_net=0, dst_host=0, payload=None)
    dummy0.send_packet(packet)
    assert dummy0.retrieve_packets()[0] is packet

    packet = Packet(id=None, src_net=0, dst_net=1, dst_host=0, payload=None)
    dummy0.send_packet(packet)
    assert dummy1.retrieve_packets()[0] is packet

    packet = Packet(id=None, src_net=0, dst_net=2, dst_host=0, payload=None)
    dummy0.send_packet(packet)
    assert dummy2.retrieve_packets()[0] is packet

def test_missing_2 ():
    router = SelectionRouter(NetInfo(-1, 0))
    dummy0 = DummyAdapter(NetInfo(0, 0))
    dummy1 = DummyAdapter(NetInfo(1, 0))

    con0 = Connection(router, dummy0)
    con1 = Connection(router, dummy1)

    router.add_interface(Interface(NetInfo(0, 0), con0))
    router.add_interface(Interface(NetInfo(1, 0), con1))

    dummy0.connect_interface(Interface(NetInfo(-1, 0), con0))
    dummy1.connect_interface(Interface(NetInfo(-1, 0), con1))

    packet = Packet(id=None, src_net=0, dst_net=0, dst_host=0, payload=None)
    dummy0.send_packet(packet)
    assert dummy0.retrieve_packets()[0] is packet

    packet = Packet(id=None, src_net=0, dst_net=1, dst_host=0, payload=None)
    dummy0.send_packet(packet)
    assert dummy1.retrieve_packets()[0] is packet

    with pytest.raises(ValueError):
        packet = Packet(id=None, src_net=0, dst_net=2, dst_host=0, payload=None)
        dummy0.send_packet(packet)

def test_too_many_2 ():
    router = SelectionRouter(NetInfo(-1, 0))
    dummy0 = DummyAdapter(NetInfo(0, 0))
    dummy1 = DummyAdapter(NetInfo(1, 0))
    dummy2 = DummyAdapter(NetInfo(2, 0))

    con0 = Connection(router, dummy0)
    con1 = Connection(router, dummy1)
    con2 = Connection(router, dummy2)

    router.add_interface(Interface(NetInfo(0, 0), con0))
    router.add_interface(Interface(NetInfo(1, 0), con1))
    router.add_interface(Interface(NetInfo(2, 0), con2))
    router.add_interface(Interface(NetInfo(2, 0), con2))

    dummy0.connect_interface(Interface(NetInfo(-1, 0), con0))
    dummy1.connect_interface(Interface(NetInfo(-1, 0), con1))
    dummy2.connect_interface(Interface(NetInfo(-1, 0), con2))

    packet = Packet(id=None, src_net=0, dst_net=0, dst_host=0, payload=None)
    dummy0.send_packet(packet)
    assert dummy0.retrieve_packets()[0] is packet

    packet = Packet(id=None, src_net=0, dst_net=1, dst_host=0, payload=None)
    dummy0.send_packet(packet)
    assert dummy1.retrieve_packets()[0] is packet

    with pytest.raises(ConnectionError):
        packet = Packet(id=None, src_net=0, dst_net=2, dst_host=0, payload=None)
        dummy0.send_packet(packet)
