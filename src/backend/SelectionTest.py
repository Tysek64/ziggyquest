from src.GUI.GameManager import GameManager
from src.backend.SelectionProcessor import SelectorProcessor
from src.backend.character_utils import load_characters
from Host import Host
from src.GUI.tracer_utils import setup_game
from PlayerProcessor import PlayerProcessor
from Switch import Switch
from pathlib import Path
from Battle import Battle
from src.GUI.drawables.ConnectionDrawable import ConnectionDrawable
from src.backend.NetInfo import NetInfo
from src.GUI.drawables.Drawable import Drawable
from threading import Thread
from src.backend.SelectionRouter import SelectionRouter
from src.GUI.StageManager import StageManager, change_to_battle
# slownik netaddr netinfo
def register_connections(arena: Battle) -> list[Drawable]:
    connections = arena.connections

    conr0 = ConnectionDrawable((400, 500), (400, 600))
    conr0.connect(connections[(0, arena.mainRouter.net_info)])

    conr1 = ConnectionDrawable((400, 500), (350, 400))
    conr1.connect(connections[(1, arena.mainRouter.net_info)])

    conp1 = ConnectionDrawable((400, 600), (350, 650))
    conp1.connect(connections[(0, NetInfo(0, 1))])
    conp2 = ConnectionDrawable((400, 600), (450, 650))
    conp2.connect(connections[(0, NetInfo(0, 2))])

    conts = ConnectionDrawable((350, 400), (400, 300))
    conts.connect(connections[(1, NetInfo(1, 1))])

    return [conr0, conr1, conp1, conp2, conts]




if __name__ == '__main__':
    selection = Battle()
    stage_manager = StageManager()
    game_manager = GameManager(stage_manager.pygame_lock, 1000, 800)
    stage_manager.set_controller(game_manager)


    character_tier_list, tiers = load_characters(Path('./characters'))

    arena = Battle()
    arena.mainRouter = SelectionRouter(NetInfo(-1,0), 'main_router')

    arena.add_switch(Switch(NetInfo(0, 0), 'net0.switch'))
    arena.add_switch(Switch(NetInfo(1, 0), 'net1.switch'))

    arena.add_host(Host(NetInfo(0, 1), 'net0.player1', PlayerProcessor()))
    arena.add_host(Host(NetInfo(0, 2), 'net0.player2', PlayerProcessor()))

    selector_processor = change_to_battle(stage_manager)(SelectorProcessor(character_tier_list, tiers))
    arena.add_host(Host(NetInfo(1, 1), 'net1.host1', selector_processor))

    drawables = register_connections(arena)

    gui_thread = Thread(target=setup_game, args=[game_manager, drawables])
    gui_thread.start()

    for _ in range(5):
        arena.mainRouter.handshake()
    gui_thread.join()