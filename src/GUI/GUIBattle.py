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
        self.active_team = 1
        self.size = self.width, self.height = window_width, window_height

        self.clock = None
        self.screen = None
        self.pygame_lock = pygame_lock
        self.winner = 0

    def check_for_click(self, rects, filters):
        while True:
            events = pygame.event.get(pygame.MOUSEBUTTONDOWN, pump=False)
            for event in events:
                pos = pygame.mouse.get_pos()
                for i, (rect, _) in enumerate(filter(filters, rects)):
                    if rect.collidepoint(pos):
                        return i
            pygame.time.delay(100)

    def get_selected_card(self):
        while self.cards[-1][-1][0] is None:
            pygame.time.delay(100)

        return 1 + self.check_for_click(self.cards[self.active_team - 1], lambda _: True)

    def get_selected_ability(self):
        while self.abilities[-1][0] is None:
            pygame.time.delay(100)

        result = self.check_for_click(self.abilities, lambda _: True)
        self.clear_abilities = True
        return result

    def create_ability(self, info):
        self.abilities.append((None, AbilityCard(info)))

    def create_character(self, team, index, info):
        if len(self.cards[team - 1]) < index:
            self.cards[team - 1].append((None, CharacterCard(team, index, info)))
        else:
            self.cards[team - 1][index - 1][1].info = info

    def run_battle(self):
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

        for i, (_, card) in enumerate(self.cards[0]):
            row_number = i // 3
            index_in_row = i % 3
            in_last_row = len(self.cards[card.team - 1]) - 3 * row_number == team_remainders[card.team - 1]

            x_pos = safe_zone_width * row_number
            y_pos = 20 + safe_zone_height * index_in_row
            offset = (self.height - (team_remainders[card.team - 1] * safe_zone_height)) / 2 if in_last_row else 0

            card_rect = card.draw(self.screen, (self.screen.get_width() - (x_pos + safe_zone_width) if card.team == 2 else x_pos) + 20, y_pos + offset, card.team == self.active_team, card_height)
            self.cards[0][i] = (card_rect, card)

        for i, (_, card) in enumerate(self.cards[1]):
            row_number = i // 3
            index_in_row = i % 3
            in_last_row = len(self.cards[card.team - 1]) - 3 * row_number == team_remainders[card.team - 1]

            x_pos = safe_zone_width * row_number
            y_pos = 20 + safe_zone_height * index_in_row
            offset = (self.height - (team_remainders[card.team - 1] * safe_zone_height)) / 2 if in_last_row else 0

            card_rect = card.draw(self.screen, (self.screen.get_width() - (x_pos + safe_zone_width) if card.team == 2 else x_pos) + 20, y_pos + offset, card.team == self.active_team, card_height)
            self.cards[1][i] = (card_rect, card)

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

    thread = threading.Thread(target=manager.run_battle, daemon=True)
    thread.start()

    while True:
        arena.mainRouter.handshake()
    manager.close()
