from pathlib import Path
from src.backend.Battle import Battle
from src.backend.character.CharacterParser import CharacterFactory
from src.backend.processors.CharacterProcessor import CharacterProcessor
from src.GUI.CharacterCard import CharacterCard, AbilityCard
from src.GUI.GUIHelper import register_player, register_selection
from src.backend.net_devices.Host import Host
from src.backend.NetInfo import NetInfo
from src.backend.processors.PlayerProcessor import PlayerProcessor
from src.backend.net_devices.Switch import Switch
from src.backend.character.character_utils import load_characters
from src.backend.net_devices.SelectionRouter import SelectionRouter
from src.GUI.GUIController import GUIController
import pygame
import sys
import threading

from src.backend.processors.SelectionProcessor import SelectionProcessor


class GUISelectionManager(GUIController):
    def __init__(self, pygame_lock, window_width=1280, window_height=720):
        super().__init__(pygame_lock, window_width, window_height)
        self.arena = Battle(SelectionRouter(NetInfo(-1, 0), 'router'))
        self.cards = []
        self.abilities = []

        self.clear_tiers = False
        self.clear_characters = False
        self.active_team = 0
        self.clock = None
        self.screen = None

    def check_for_click(self, rects):
        while True:
            events = pygame.event.get(pygame.MOUSEBUTTONDOWN, pump=False)
            for event in events:
                pos = pygame.mouse.get_pos()
                for i, (rect, _) in enumerate(rects):
                    if rect.collidepoint(pos):
                        return i
            pygame.time.delay(100)

    def get_selected_card(self):
        while len(self.cards) == 0 or self.cards[-1][0] is None:
            pygame.time.delay(100)

        result = self.check_for_click(self.cards)
        self.clear_characters = True
        return result

    def get_selected_ability(self):
        while len(self.abilities) == 0 or self.abilities[-1][0] is None:
            pygame.time.delay(100)

        result = self.check_for_click(self.abilities)
        self.clear_tiers = True
        return result

    def create_tier(self, info):
        print(info)
        self.abilities.append((None, AbilityCard(info)))

    def create_character(self, info):
        print('INFO\n', info, '\nINFO')
        self.cards.append((None, AbilityCard(info)))

    def setup(self, *args, **kwargs):
        @register_player(self)
        def create_player(): return PlayerProcessor()

        characters, tiers = load_characters(kwargs['character_root_path'])

        @register_selection(self)
        def create_selection(): return SelectionProcessor(characters, tiers)

        for i in range(2):
            self.arena.add_switch(Switch(NetInfo(i, 0), f'net{i}.switch'))

        self.arena.add_host(Host(NetInfo(1, 1), 'net1.host1', create_selection()))

        self.arena.add_host(Host(NetInfo(0, 1), 'net0.player1', create_player()))
        self.arena.add_host(Host(NetInfo(0, 2), 'net0.player2', create_player()))


    def run(self):
        running = True

        with self.pygame_lock:
            pygame.init()
            self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
            self.clock = pygame.time.Clock()

            # self.cards = [(None, CharacterCard(host.net_info.net_addr, host.net_info.host_addr, host.packet_processor))
            #               for host in self.arena.hosts.values() if
            #               isinstance(host.packet_processor, CharacterProcessor)]
            self.cards = []

            while running:
                running = len(pygame.event.get(pygame.QUIT)) == 0
                self.size = self.width, self.height = self.screen.get_width(), self.screen.get_height()
                
                self.render_battlefield()

                if not self.arena.mainRouter.handshake_running:
                    thread = threading.Thread(target=self.arena.mainRouter.handshake, daemon=True)
                    thread.start()

                if self.clear_tiers:
                    self.abilities = []
                    self.clear_tiers = False

                if self.clear_characters:
                    self.cards = []
                    self.clear_characters = False

                pygame.display.update()
                self.clock.tick(60)

            self.close()

    def render_battlefield(self):
        self.screen.fill('ivory3')

        for i, (_, card) in enumerate(self.cards):
            card_rect = card.draw(self.screen, self.width / 2 - 250, self.height / 2 - (len(self.abilities) / 2) * 75 + i * 75)
            self.cards[i] = (card_rect, card)

        for i, (_, ability) in enumerate(self.abilities):
            card_rect = ability.draw(self.screen, self.width / 2 - 250, self.height / 2 - (len(self.abilities) / 2) * 75 + i * 75)
            self.abilities[i] = (card_rect, ability)

    def close(self):
        pygame.quit()
        sys.exit()

if __name__ == '__main__':

    manager = GUISelectionManager(threading.Lock())
    manager.setup(character_root_path=Path('./characters'))
    manager.run()

