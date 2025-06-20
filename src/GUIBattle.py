from Battle import Battle
from GUI.CharacterCard import CharacterCard, AbilityCard
import pygame
from CharacterParser import CharacterFactory
from CharacterProcessor import CharacterProcessor
from Host import Host
from NetInfo import NetInfo
from PlayerProcessor import PlayerProcessor
from Switch import Switch
from pathlib import Path
from GUIHelper import register_player, register_character
from GUI.GUISettings import X_SIZE, Y_SIZE
import threading

class GUIBattleManager:
    def __init__(self):
        self.arena = Battle()
        self.cards = []
        self.abilities = []
        self.active_team = 0

        self.running = False
        self.clock = None
        self.screen = None

    def check_for_click(self, rects):
        while True:
            event = pygame.event.wait(100)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, rect in enumerate(rects):
                    if rect.collidepoint(pos):
                        return i
            else:
                pygame.event.post(event)
        return None

    def get_selected_card(self):
        while self.cards[-1][0] is None:
            pygame.time.delay(100)

        return 1 + self.check_for_click([rect for rect, card in self.cards if card.team == self.active_team])

    def get_selected_ability(self):
        while self.abilities[-1][0] is None:
            pygame.time.delay(100)

        result = self.check_for_click([rect for rect, _ in self.abilities])
        self.abilities = []
        return result

    def create_ability(self, info):
        self.abilities.append((None, AbilityCard(self.screen, info)))

    def setup_battle(self, team_1, team_2):
        @register_player(self)
        def create_player():
            return PlayerProcessor()

        @register_character(self)
        def create_character(character):
            return(CharacterProcessor(character))

        self.arena = Battle()

        self.arena.add_switch(Switch(NetInfo(1, 0), 'net1.switch'))
        self.arena.add_switch(Switch(NetInfo(2, 0), 'net2.switch'))
        self.arena.add_switch(Switch(NetInfo(0, 0), 'net0.switch'))

        for i, character in enumerate(team_1, start=1):
            self.arena.add_host(Host(NetInfo(1, i), f'net1.host{i}', create_character(character)))

        for i, character in enumerate(team_2, start=1):
            self.arena.add_host(Host(NetInfo(2, i), f'net2.host{i}', create_character(character)))

        self.arena.add_host(Host(NetInfo(0, 1), 'net0.player1', create_player()))
        self.arena.add_host(Host(NetInfo(0, 2), 'net0.player2', create_player()))

    def init_battle(self):
        pygame.init()
        self.screen = pygame.display.set_mode((X_SIZE, Y_SIZE))
        self.clock = pygame.time.Clock()
        self.running = True

        self.cards = [(None, CharacterCard(self.screen, host.net_info.net_addr, host.net_info.host_addr, host.packet_processor)) for host in self.arena.hosts.values() if isinstance(host.packet_processor, CharacterProcessor)]

    def start_battle(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill('ivory3')

            team_counters = {card.team: 0 for _, card in self.cards}

            for i, (_, card) in enumerate(self.cards):
                card_rect = card.draw(100 if card.team == 1 else X_SIZE - 300, 50 + 350 * team_counters[card.team], card.team == self.active_team)
                team_counters[card.team] += 1

                self.cards[i] = (card_rect, card)

            for i, (_, ability) in enumerate(self.abilities):
                card_rect = ability.draw(X_SIZE / 2 - 250, Y_SIZE / 2 - (len(self.abilities) / 2) * 75 + i * 75)
                self.abilities[i] = (card_rect, ability)

            pygame.display.flip()

            if not self.arena.mainRouter.current_move[0]:
                thread = threading.Thread(target=self.arena.mainRouter.handshake, daemon=True)
                thread.start()

            self.clock.tick(60)

        self.end_battle()

    def end_battle(self):
        pygame.quit()

if __name__ == '__main__':
    characters = CharacterFactory().make_characters(Path('./characters'))
    ziggy = characters[0]
    kibel = characters[1]
    cofee = characters[2]

    manager = GUIBattleManager()
    manager.setup_battle([ziggy, ziggy], [kibel, kibel, kibel])
    manager.init_battle()
    manager.start_battle()
