from Battle import Battle
from GUI.CharacterCard import CharacterCard
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

    def get_selected_card(self):
        while True:
            event = pygame.event.wait(100)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for rect, card in self.cards:
                    if rect.collidepoint(pos) and card.team == self.active_team:
                        print('a')
                        return card.index
            else:
                pygame.event.post(event)

    def get_selected_ability(self):
        while True:
            event = pygame.event.wait(100)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, (rect, ability) in enumerate(self.abilities):
                    if rect.collidepoint(pos):
                        self.abilities = []
                        return i
            else:
                pygame.event.post(event)

    def setup_battle(self):
        @register_player(self)
        def create_player():
            return PlayerProcessor()

        @register_character(self)
        def create_character(character):
            return(CharacterProcessor(character))

        ziggy = CharacterFactory().make_characters(Path('./characters'))[0]
        kibel = CharacterFactory().make_characters(Path('./characters'))[1]
        cofee = CharacterFactory().make_characters(Path('./characters'))[2]

        self.arena = Battle()

        self.arena.add_switch(Switch(NetInfo(1, 0), 'net1.switch'))
        self.arena.add_switch(Switch(NetInfo(2, 0), 'net2.switch'))
        self.arena.add_switch(Switch(NetInfo(0, 0), 'net0.switch'))

        self.arena.add_host(Host(NetInfo(1, 1), 'net1.host1', create_character(ziggy)))
        self.arena.add_host(Host(NetInfo(1, 2), 'net1.host2', create_character(ziggy)))
        self.arena.add_host(Host(NetInfo(2, 1), 'net2.host1', create_character(kibel)))
        self.arena.add_host(Host(NetInfo(2, 2), 'net2.host2', create_character(kibel)))

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

            thread = threading.Thread(target=self.arena.mainRouter.handshake, daemon=True)
            thread.start()

            self.clock.tick(60)

        self.end_battle()

    def end_battle(self):
        pygame.quit()

if __name__ == '__main__':
    manager = GUIBattleManager()
    manager.setup_battle()
    manager.init_battle()
    manager.start_battle()
