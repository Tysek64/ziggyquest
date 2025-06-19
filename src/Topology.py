from CharacterParser import CharacterFactory
from CharacterProcessor import CharacterProcessor
from Host import Host
from NetInfo import NetInfo
from PlayerProcessor import PlayerProcessor
from Switch import Switch
from pathlib import Path
from Battle import Battle

if __name__ == '__main__':
    character = CharacterFactory().make_characters(Path('./characters'))[0]

    arena = Battle()

    arena.add_switch(Switch(NetInfo(1, 0), 'net1.switch'))
    arena.add_switch(Switch(NetInfo(2, 0), 'net2.switch'))
    arena.add_switch(Switch(NetInfo(0, 0), 'net0.switch'))

    arena.add_host(Host(NetInfo(1, 1), 'net1.host1', CharacterProcessor(character)))
    arena.add_host(Host(NetInfo(1, 2), 'net1.host2', CharacterProcessor(character)))
    arena.add_host(Host(NetInfo(2, 1), 'net2.host1', CharacterProcessor(character)))
    arena.add_host(Host(NetInfo(2, 2), 'net2.host2', CharacterProcessor(character)))

    arena.add_host(Host(NetInfo(0, 1), 'net0.player1', PlayerProcessor()))
    arena.add_host(Host(NetInfo(0, 2), 'net0.player2', PlayerProcessor()))

    for i in range(10):
        arena.mainRouter.handshake()
