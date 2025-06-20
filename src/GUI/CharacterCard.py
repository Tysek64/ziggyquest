import pygame.draw
import pygame
import urllib.request
import io
import GUI.GUIInput

class CharacterCard:
    def __init__(self, context, team, index, followed_processor):
        self.ctx = context
        self.team = team
        self.index = index
        self.processor = followed_processor

        if self.processor.base_character.loaded_image is None:
            url = self.processor.base_character.img_link
            print(f'Fetching profile pic from {url}...')
            request = urllib.request.urlopen(url)

            self.processor.base_character.loaded_image = request.read()
        else:
            print(f'Profile pic for {self.processor.base_character.name} has already been fetched!')

    def draw(self, x, y):
        card_rect = pygame.draw.rect(self.ctx, 'lightpink1' if GUI.GUIInput.active_team == self.team else 'ivory4' , pygame.Rect(x, y, 200, 300))
        font = pygame.font.SysFont('monospace', 24)

        label = font.render(self.processor.character_state.name, 1, 'black')
        self.ctx.blit(label, (x + 10, y + 10))

        label = font.render(f'HP: {self.processor.character_state.hp}', 1, 'black')
        self.ctx.blit(label, (x + 10, y + 150))

        label = font.render(f'MP: {self.processor.character_state.mp}', 1, 'black')
        self.ctx.blit(label, (x + 10, y + 190))

        image = pygame.image.load(io.BytesIO(self.processor.base_character.loaded_image))
        image = pygame.transform.scale(image, (180, 180 * image.get_height() / image.get_width()))

        self.ctx.blit(image, (x + 10, y + 40), (0, image.get_height() / 2 - 50, 180, 100))

        return card_rect

class AbilityCard:
    def __init__(self, context, info):
        self.ctx = context
        self.info = info

    def draw(self, x, y):
        card_rect = pygame.draw.rect(self.ctx, 'lightpink1', pygame.Rect(x, y, 500, 50))
        font = pygame.font.SysFont('monospace', 24)

        label = font.render(self.info, 1, 'black')
        self.ctx.blit(label, (x + 10, y + 10))

        return card_rect
