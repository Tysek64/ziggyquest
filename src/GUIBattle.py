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
import GUI.GUIInput
import threading

def setup_battle():
    @register_player
    def create_player():
        return PlayerProcessor()

    @register_character
    def create_character(character):
        return(CharacterProcessor(character))

    ziggy = CharacterFactory().make_characters(Path('./characters'))[0]
    kibel = CharacterFactory().make_characters(Path('./characters'))[1]
    cofee = CharacterFactory().make_characters(Path('./characters'))[2]

    arena = Battle()

    arena.add_switch(Switch(NetInfo(1, 0), 'net1.switch'))
    arena.add_switch(Switch(NetInfo(2, 0), 'net2.switch'))
    arena.add_switch(Switch(NetInfo(0, 0), 'net0.switch'))

    arena.add_host(Host(NetInfo(1, 1), 'net1.host1', create_character(ziggy)))
    arena.add_host(Host(NetInfo(1, 2), 'net1.host2', create_character(ziggy)))
    arena.add_host(Host(NetInfo(2, 1), 'net2.host1', create_character(kibel)))
    arena.add_host(Host(NetInfo(2, 2), 'net2.host2', create_character(kibel)))

    arena.add_host(Host(NetInfo(0, 1), 'net0.player1', create_player()))
    arena.add_host(Host(NetInfo(0, 2), 'net0.player2', create_player()))

    return arena

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((X_SIZE, Y_SIZE))
    clock = pygame.time.Clock()
    running = True

    arena = setup_battle()
    GUI.GUIInput.cards = [(None, CharacterCard(screen, host.net_info.net_addr, host.net_info.host_addr, host.packet_processor)) for host in arena.hosts.values() if isinstance(host.packet_processor, CharacterProcessor)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill('ivory3')

        team_counters = {card.team: 0 for _, card in GUI.GUIInput.cards}

        for i, (_, card) in enumerate(GUI.GUIInput.cards):
            card_rect = card.draw(100 if card.team == 1 else X_SIZE - 300, 50 + 350 * team_counters[card.team])
            team_counters[card.team] += 1

            GUI.GUIInput.cards[i] = (card_rect, card)

        for i, (_, ability) in enumerate(GUI.GUIInput.abilities):
            card_rect = ability.draw(X_SIZE / 2 - 250, Y_SIZE / 2 - (len(GUI.GUIInput.abilities) / 2) * 75 + i * 75)
            GUI.GUIInput.abilities[i] = (card_rect, ability)

        pygame.display.flip()

        thread = threading.Thread(target=arena.mainRouter.handshake, daemon=True)
        thread.start()
        #arena.mainRouter.handshake()
        clock.tick(60)

    pygame.quit()

