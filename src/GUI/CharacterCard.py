from src.GUI.ImageCache import ImageCache
import pygame.draw
import pygame
import io
import json

class CharacterCard:
    def __init__(self, team, index, info):
        self.team = team
        self.index = index
        self.info = json.loads(info)

        self.image = ImageCache.fetch_image(self.info['checksum'], self.info['img_link'])

    def set_info(self, info=None):
        if info is not None:
            prev_image = self.info['checksum']
            self.info = json.loads(info)
            if prev_image != self.info['checksum']:
                print('???')
                self.image = ImageCache.fetch_image(self.info['checksum'], self.info['img_link'])

    def draw(self, ctx, x, y, active, allowed_height=300, info=None):
        if info is not None:
            self.info = json.loads(info)

        allowed_width = 2 * allowed_height / 3
        base_margin = 0.05 * allowed_width
        inner_margin = 0.6 * base_margin

        font_size = int(2 * allowed_height / 25)

        image_width = allowed_width - 2 * base_margin
        image_height = 5 * image_width / 9

        text_offset = font_size + inner_margin
        image_offset = image_height + inner_margin

        card_rect = pygame.draw.rect(ctx, 'ivory4' if self.info['hp'] == 0 else ('lightpink1' if active else 'ivory4') , pygame.Rect(x, y, allowed_width, allowed_height))
        font = pygame.font.SysFont('monospace', font_size)
        bold_font = pygame.font.SysFont('monospace', bold=True, size=font_size)

        label = bold_font.render(self.info['name'], 1, 'black')
        ctx.blit(label, (x + base_margin, y + base_margin))

        label = font.render(f'HP: {self.info['hp']}', 1, 'black')
        ctx.blit(label, (x + base_margin, y + base_margin + text_offset + image_offset))

        label = font.render(f'MP: {self.info['mp']}', 1, 'black')
        ctx.blit(label, (x + base_margin, y + base_margin + 2 * text_offset + image_offset))

        image = pygame.image.load(io.BytesIO(self.image))
        image = pygame.transform.scale(image, (image_width, image_width * image.get_height() / image.get_width()))

        ctx.blit(image, (x + base_margin, y + base_margin + text_offset), (0, (image.get_height() - image_height) / 2, image_width, image_height))

        return card_rect

    def __str__(self):
        return str(self.info)

    def __repr__(self):
        return str(self.info)

class AbilityCard:
    def __init__(self, info):
        self.info = info

    def draw(self, ctx, x, y):
        card_rect = pygame.draw.rect(ctx, 'ivory4' if self.info == '' or self.info[0] == '-' else 'lightpink1', pygame.Rect(x, y, 500, 50))
        font = pygame.font.SysFont('monospace', 24)

        label = font.render(self.info, 1, 'black')
        ctx.blit(label, (x + 10, y + 10))

        return card_rect
