from CharacterCard import CharacterCard
import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

testCharacter = CharacterCard(screen)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    testCharacter.draw(100, 100)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
