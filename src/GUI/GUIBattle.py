from pathlib import Path
from src.backend.Battle import Battle
from src.backend.CharacterParser import CharacterFactory
from src.backend.CharacterProcessor import CharacterProcessor
from src.GUI.CharacterCard import CharacterCard, AbilityCard
from src.GUI.GUIHelper import register_player, register_character
from src.backend.Host import Host
from src.backend.NetInfo import NetInfo
from src.backend.PlayerProcessor import PlayerProcessor
from src.backend.Switch import Switch
import pygame
import sys
import threading

class GUIBattleManager:
    def __init__(self, pygame_lock, window_width=1280, window_height=720):
        self.arena = Battle()
        self.cards = []
        self.abilities = []
        self.active_team = 0
        self.size = self.width, self.height = window_width, window_height
        self.team_lens = (0, 0)

        self.clock = None
        self.screen = None
        self.pygame_lock = pygame_lock

    def check_for_click(self, rects):
        while True:
            events = pygame.event.get(pygame.MOUSEBUTTONDOWN, pump=False)
            for event in events:
                pos = pygame.mouse.get_pos()
                for i, (rect, _) in enumerate(rects):
                    if rect.collidepoint(pos):
                        return i
            pygame.time.delay(100)
        return None

    def get_selected_card(self):
        while self.cards[-1][0] is None:
            pygame.time.delay(100)

        return 1 + self.check_for_click([(rect, card) for rect, card in self.cards if card.team == self.active_team])

    def get_selected_ability(self):
        while self.abilities[-1][0] is None:
            pygame.time.delay(100)

        result = self.check_for_click(self.abilities)
        self.abilities = []
        return result

    def create_ability(self, info):
        self.abilities.append((None, AbilityCard(self.screen, info)))

    def setup_battle(self, team_1, team_2):
        @register_player(self)
        def create_player(): return PlayerProcessor()

        @register_character(self)
        def create_character(character): return CharacterProcessor(character)

        for i in range(3):
            self.arena.add_switch(Switch(NetInfo(i, 0), f'net{i}.switch'))

        for i, character in enumerate(team_1, start=1):
            self.arena.add_host(Host(NetInfo(1, i), f'net1.host{i}', create_character(character)))

        for i, character in enumerate(team_2, start=1):
            self.arena.add_host(Host(NetInfo(2, i), f'net2.host{i}', create_character(character)))

        self.arena.add_host(Host(NetInfo(0, 1), 'net0.player1', create_player()))
        self.arena.add_host(Host(NetInfo(0, 2), 'net0.player2', create_player()))

        self.team_lens = (len(team_1), len(team_2))

    def init_battle(self):
        pass

    def run_battle(self):
        running = True

        with self.pygame_lock:
            pygame.init()
            self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
            self.clock = pygame.time.Clock()

            self.cards = [(None, CharacterCard(host.net_info.net_addr, host.net_info.host_addr, host.packet_processor))
                          for host in self.arena.hosts.values() if
                          isinstance(host.packet_processor, CharacterProcessor)]

            while running:
                running = len(pygame.event.get(pygame.QUIT)) == 0

                self.size = self.width, self.height = self.screen.get_width(), self.screen.get_height()

                self.render_battlefield()

                if not self.arena.mainRouter.current_move[0]:
                    thread = threading.Thread(target=self.arena.mainRouter.handshake, daemon=True)
                    thread.start()

                pygame.display.update()
                self.clock.tick(60)
            self.close()

    def render_battlefield(self):
        self.screen.fill('ivory3')

        team_counters = {card.team: 0 for _, card in self.cards}

        for i, (_, card) in enumerate(self.cards):
            safe_zone_height = self.height / self.team_lens[card.team - 1]
            card_height = safe_zone_height - 40
            card_width = 2 * card_height / 3

            card_rect = card.draw(self.screen, 100 if card.team == 1 else self.width - 100 - card_width, 20 + safe_zone_height * team_counters[card.team], card.team == self.active_team, card_height)
            self.cards[i] = (card_rect, card)

            team_counters[card.team] += 1

        for i, (_, ability) in enumerate(self.abilities):
            card_rect = ability.draw(self.width / 2 - 250, self.height / 2 - (len(self.abilities) / 2) * 75 + i * 75)
            self.abilities[i] = (card_rect, ability)

    def close(self):
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    [ziggy, kibel, cofee] = CharacterFactory().make_characters(Path('./characters'))

    manager = GUIBattleManager()
    manager.setup_battle([ziggy, ziggy], [kibel, kibel, kibel])
    manager.init_battle()
    manager.run_battle()
    manager.end_battle()
