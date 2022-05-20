import pygame


class button:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, self.sprite_w, self.sprite_h)
