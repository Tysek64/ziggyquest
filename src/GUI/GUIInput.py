import pygame
import asyncio

cards = []
abilities = []
active_team = 0

def get_selected_card():
    global cards
    while True:
        event = pygame.event.wait(100)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for rect, card in cards:
                if rect.collidepoint(pos) and card.team == active_team:
                    print('a')
                    return card.index
        else:
            pygame.event.post(event)

def get_selected_ability():
    global abilities
    while True:
        event = pygame.event.wait(100)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for i, (rect, ability) in enumerate(abilities):
                if rect.collidepoint(pos):
                    abilities = []
                    return i
        else:
            pygame.event.post(event)
