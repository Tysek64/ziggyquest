import argparse
from src.GUI.GUIBattle import GUIBattleManager
from src.backend.processors.ServerSocket import ServerSocket
from src.backend.processors.ClientSocket import ClientSocket
from src.backend.character.CharacterParser import CharacterFactory
from src.backend.Battle import Battle
from src.GUI.GUIHelper import register_player
from src.backend.net_devices.Switch import Switch
from src.backend.net_devices.Host import Host
from src.backend.NetInfo import NetInfo
from src.backend.processors.PlayerProcessor import PlayerProcessor
from src.backend.processors.CharacterProcessor import CharacterProcessor
from pathlib import Path
import threading

def setup_server(ip_addr):
    [ziggy, kibel, cofee] = CharacterFactory().make_characters(Path('./characters'))

    manager = GUIBattleManager(threading.Lock())
    arena = Battle()

    @register_player(manager)
    def create_player(): return PlayerProcessor()

    for i in range(3):
        arena.add_switch(Switch(NetInfo(i, 0), f'net{i}.switch'))

    for i, character in enumerate([ziggy, cofee], start=1):
        arena.add_host(Host(NetInfo(1, i), f'net1.host{i}', CharacterProcessor(character)))

    for i, character in enumerate([kibel, kibel, kibel], start=1):
        arena.add_host(Host(NetInfo(2, i), f'net2.host{i}', CharacterProcessor(character)))

    arena.add_host(Host(NetInfo(0, 1), 'net0.player1', ServerSocket(ip_addr=ip_addr)))
    arena.add_host(Host(NetInfo(0, 2), 'net0.player2', create_player()))

    def run():
        while True:
            arena.mainRouter.handshake()

    thread = threading.Thread(target=run)
    thread.start()

    manager.run_battle()

    manager.close()
    sys.exit()

def setup_client(ip_addr):
    manager = GUIBattleManager(threading.Lock())

    @register_player(manager)
    def create_player(): return PlayerProcessor()

    arena = ClientSocket(ip_addr=ip_addr, processor=create_player())

    thread = threading.Thread(target=manager.run_battle)
    thread.start()

    def run():
        while True:
            arena.receive_packet()

    thread = threading.Thread(target=run)
    thread.start()

    manager.run_battle()

    manager.close()
    sys.exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--server', '-s', action='store_true')
    parser.add_argument('ip_addr')

    args = parser.parse_args()

    if args.server:
        setup_server(args.ip_addr)
    else:
        setup_client(args.ip_addr)
