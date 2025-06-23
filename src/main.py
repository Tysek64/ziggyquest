import argparse
from src.GUI.GUIBattle import GUIBattleManager
from src.backend.processors.ServerSocket import ServerSocket
from src.backend.processors.ClientSocket import ClientSocket
from src.backend.character.CharacterParser import CharacterFactory
from src.backend.character.character_utils import load_characters
from src.backend.Battle import Battle
from src.GUI.GUIHelper import register_player
from src.backend.net_devices.Switch import Switch
from src.backend.net_devices.Host import Host
from src.backend.net_devices.SelectionRouter import SelectionRouter
from src.backend.NetInfo import NetInfo
from src.backend.processors.PlayerProcessor import PlayerProcessor
from src.backend.processors.CharacterProcessor import CharacterProcessor
from src.backend.processors.SelectionProcessor import SelectionProcessor
from pathlib import Path
import threading

def setup_server(ip_addr, single_player=False):
    [ziggy, kibel, cofee] = CharacterFactory().make_characters(Path('./characters'))

    manager = GUIBattleManager(threading.Lock())
    arena = Battle(SelectionRouter(NetInfo(-1, 1), hostname='router'))
    characters, tiers = load_characters(Path('./characters'))

    @register_player(manager)
    def create_player(): return PlayerProcessor()

    for i in range(2):
        arena.add_switch(Switch(NetInfo(i, 0), f'net{i}.switch'))

    '''
    for i, character in enumerate([ziggy, cofee], start=1):
        arena.add_host(Host(NetInfo(1, i), f'net1.host{i}', CharacterProcessor(character)))

    for i, character in enumerate([kibel, kibel, kibel], start=1):
        arena.add_host(Host(NetInfo(2, i), f'net2.host{i}', CharacterProcessor(character)))
    '''

    selector = SelectionProcessor(characters, tiers)
    player1 = create_player() if single_player else ServerSocket(ip_addr=ip_addr)
    player2 = create_player()

    arena.add_host(Host(NetInfo(1, 1), 'net1.host1', selector))
    arena.add_host(Host(NetInfo(0, 1), 'net0.player1', player1))
    arena.add_host(Host(NetInfo(0, 2), 'net0.player2', player2))

    selecting = True

    def change_topology(team1, team2):
        nonlocal arena
        nonlocal selecting
        selecting = False
        arena = Battle()

        @register_player(manager)
        def create_player(): return PlayerProcessor()

        for i in range(3):
            arena.add_switch(Switch(NetInfo(i, 0), f'net{i}.switch'))

        for i, character in enumerate(team1, start=1):
            arena.add_host(Host(NetInfo(1, i), f'net1.host{i}', CharacterProcessor(character)))

        for i, character in enumerate(team2, start=1):
            arena.add_host(Host(NetInfo(2, i), f'net2.host{i}', CharacterProcessor(character)))

        arena.add_host(Host(NetInfo(0, 1), 'net0.player1', player1))
        arena.add_host(Host(NetInfo(0, 2), 'net0.player2', player2))

    def run():
        nonlocal arena
        while True:
            arena.mainRouter.handshake()

            if selecting and selector.notify_change_stage():
                manager.clear_cards = True
                manager.clear_abilities = True
                change_topology(selector.teams[1], selector.teams[2])
                arena.print_status()

    thread = threading.Thread(target=run, daemon=True)
    thread.start()

    manager.run_battle()

    manager.close()
    sys.exit()

def setup_client(ip_addr):
    manager = GUIBattleManager(threading.Lock())

    @register_player(manager)
    def create_player(): return PlayerProcessor()

    arena = ClientSocket(ip_addr=ip_addr, processor=create_player())

    def run():
        while True:
            arena.receive_packet()

    thread = threading.Thread(target=run, daemon=True)
    thread.start()

    manager.run_battle()

    manager.close()
    sys.exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--server', '-s', action='store_true')
    parser.add_argument('--no_network', '-n', action='store_true')
    parser.add_argument('ip_addr')

    args = parser.parse_args()

    if args.server:
        setup_server(args.ip_addr)
    elif args.no_network:
        setup_server(args.ip_addr, True)
    else:
        setup_client(args.ip_addr)
