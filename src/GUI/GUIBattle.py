from pathlib import Path
from src.backend.Battle import Battle
from src.backend.character.CharacterParser import CharacterFactory
from src.backend.processors.CharacterProcessor import CharacterProcessor
from src.GUI.CharacterCard import CharacterCard, AbilityCard
from src.GUI.GUIHelper import register_player
from src.backend.net_devices.Host import Host
from src.backend.NetInfo import NetInfo
from src.backend.processors.PlayerProcessor import PlayerProcessor
from src.backend.processors.ServerSocket import ServerSocket
from src.backend.net_devices.Switch import Switch
import pygame
import sys
import threading
from src.GUI.GUIController import GUIController
class GUIBattleManager(GUIController):
    def __init__(self, pygame_lock, window_width=1280, window_height=720):
        self.cards = [[], []]
        self.abilities = []
        self.clear_abilities = False
        self.clear_cards = False
        self.in_battle = False
        self.active_team = 1
        self.active = False
        self.size = self.width, self.height = window_width, window_height

        self.clock = None
        self.screen = None
        self.pygame_lock = pygame_lock
        self.winner = 0

    def transfer_to_battle(self):
        self.in_battle = True
        self.abilities = []
        self.cards = [[], []]

    def check_for_click(self, rects, filter=lambda rect, card: True):
        while True:
            events = pygame.event.get(pygame.MOUSEBUTTONDOWN, pump=False)
            for event in events:
                pos = pygame.mouse.get_pos()
                for i, (rect, card) in enumerate(rects):
                    if rect.collidepoint(pos) and filter(rect, card):
                        return i
            pygame.time.delay(100)

    def get_selected_card(self):
        if not self.in_battle:
            self.active_team = 1

        while len(self.cards[self.active_team - 1]) == 0 or self.cards[self.active_team - 1][-1][0] is None:
            pygame.time.delay(100)

        result = 1 + self.check_for_click(self.cards[self.active_team - 1], lambda rect, card: card.info['hp'] > 0)
        self.clear_cards = True
        return result

    def get_selected_ability(self):
        while len(self.abilities) == 0 or self.abilities[-1][0] is None:
            pygame.time.delay(100)

        result = self.check_for_click(self.abilities, lambda rect, card: card.info != '' and card.info[0] != '-')
        self.clear_abilities = True
        return result

    def create_ability(self, info):
        self.abilities.append((None, AbilityCard(info)))

    def create_character(self, team, index, info):
        if len(self.cards[team - 1]) < index:
            for i in range(index - len(self.cards[team - 1])):
                self.cards[team - 1].append((None, CharacterCard(team, index, info)))
        else:
            self.cards[team - 1][index - 1][1].set_info(info)

    def setup(self, *args, **kwargs):
        pass

    def run(self):
        running = True

        with self.pygame_lock:
            pygame.init()
            self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
            self.clock = pygame.time.Clock()

            while running:
                running = len(pygame.event.get(pygame.QUIT)) == 0
                self.size = self.width, self.height = self.screen.get_width(), self.screen.get_height()
                
                if self.winner == 0:
                    self.render_battlefield()

                    if self.clear_abilities:
                        self.abilities = []
                        self.clear_abilities = False

                    if self.clear_cards and not self.in_battle:
                        self.cards = [[], []]
                        self.clear_cards = False
                else:
                    self.render_end_screen()

                pygame.display.update()
                self.clock.tick(60)

            self.close()

    def render_battlefield(self):
        self.screen.fill('ivory3')

        team_remainders = [len(cards) % 3 for cards in self.cards]

        safe_zone_height = self.height / 3
        card_height = max(0, safe_zone_height - 40)
        card_width = 2 * card_height / 3
        safe_zone_width = card_width + 40

        for j, cards in enumerate(self.cards):
            for i, (_, card) in enumerate(self.cards[j]):
                row_number = i // 3
                index_in_row = i % 3
                in_last_row = len(cards) - 3 * row_number == team_remainders[j]

                x_pos = safe_zone_width * row_number
                y_pos = 20 + safe_zone_height * index_in_row
                offset = (self.height - (team_remainders[j] * safe_zone_height)) / 2 if in_last_row else 0

                card_rect = card.draw(self.screen, (self.screen.get_width() - (x_pos + safe_zone_width) if card.team == 2 else x_pos) + 20, y_pos + offset, (card.team == self.active_team) and self.active, card_height)
                self.cards[j][i] = (card_rect, card)

        for i, (_, ability) in enumerate(self.abilities):
            card_rect = ability.draw(self.screen, self.width / 2 - 250, self.height / 2 - (len(self.abilities) / 2) * 75 + i * 75)
            self.abilities[i] = (card_rect, ability)

    def render_end_screen(self):
        self.screen.fill('black')

        font = pygame.font.SysFont('serif', bold=True, size=72)

        label = font.render(f'Player {self.winner} won!', 1, 'darkgoldenrod')
        rect = label.get_rect()

        self.screen.blit(label, ((self.width - rect.width) / 2, (self.height - rect.height) / 2))

    def announce_winner(self, winning_team):
        print(f'Team {winning_team} won!')
        self.winner = winning_team

    def close(self):
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    [ziggy, kibel, cofee] = CharacterFactory().make_characters(Path('./characters'))

    manager = GUIBattleManager(threading.Lock())
    arena = Battle()

    @register_player(manager)
    def create_player(): return PlayerProcessor()

    for i in range(3):
        arena.add_switch(Switch(NetInfo(i, 0), f'net{i}.switch'))

    for i, character in enumerate([ziggy, cofee], start=1):
        arena.add_host(Host(NetInfo(1, i), f'net1.host{i}', CharacterProcessor(character)))

    for i, character in enumerate([kibel], start=1):
        arena.add_host(Host(NetInfo(2, i), f'net2.host{i}', CharacterProcessor(character)))

    arena.add_host(Host(NetInfo(0, 1), 'net0.player1', create_player()))
    arena.add_host(Host(NetInfo(0, 2), 'net0.player2', create_player()))

    thread = threading.Thread(target=manager.run, daemon=True)
    thread.start()

    while True:
        arena.mainRouter.handshake()
    manager.close()
