import pygame
import my_utils
from spritesheet import Spritesheet


class Button:
    def __init__(self, x, y, text):
        self.sprite_w = 260
        self.sprite_h = 52
        self.rect = pygame.Rect(
            x - self.sprite_w / 2, y - self.sprite_h / 2, self.sprite_w, self.sprite_h
        )
        self.sprites = Spritesheet.parse_button_sprites(Spritesheet)
        self.text = text
        self.is_pressed = False

    def draw(self):
        """
        Return a surface with the button drawn on it
        """
        surface = pygame.Surface((self.sprite_w, self.sprite_h))
        if self.is_pressed:
            surface.blit(self.sprites["button_pressed"], (0, 0))
            my_utils.draw_centered_text(
                surface,
                self.text,
                30,
                surface.get_rect().centerx + 2,
                surface.get_rect().centery + 2,
            )
        else:
            surface.blit(self.sprites["button"], (0, 0))
            my_utils.draw_centered_text(
                surface,
                self.text,
                30,
                surface.get_rect().centerx,
                surface.get_rect().centery,
            )
        return surface
