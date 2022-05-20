from spritesheet import Spritesheet
from gamestate import GameState
import pygame


class Status:
    """
    Defines a numerical display object; The numbers showing the bombs left and
    the amount of seconds elapsed.
    Emulates a 3 digit LED display.
    """

    def __init__(self, x, y):
        self.num = 0
        self.sprite_w = 26
        self.sprite_h = 46
        self.rect = (x, y, self.sprite_w * 3, self.sprite_h)
        self.sprites = Spritesheet.parse_number_sprites(Spritesheet)

    def update(self, number):
        """
        Updates object with an integer to display
        """
        self.num = number

    def draw(self):
        """
        Returns a surface with the numerical display
        """
        surface = pygame.Surface((self.sprite_w * 3, self.sprite_h))

        first_digit = (self.num % 1000) // 100
        second_digit = (self.num % 100) // 10
        third_digit = self.num % 10
        if self.num >= 10:
            if third_digit == 0:
                third_digit = 10
        if self.num >= 100:
            if second_digit == 0:
                second_digit = 10

        surface.blit(self.sprites[first_digit], (0, 0))
        surface.blit(self.sprites[second_digit], (self.sprite_w, 0))
        surface.blit(self.sprites[third_digit], (2 * self.sprite_w, 0))
        return surface


class Faces:
    """
    Defines the top bar game state face indicator
    """

    def __init__(self, x, y):
        self.sprite_w = 52
        self.sprite_h = 52
        self.rect = pygame.Rect(x, y, self.sprite_w, self.sprite_h)
        self.sprites = Spritesheet.parse_face_sprites(Spritesheet)

    def draw(self, game_state, pressed):
        """
        Returns a surface with the face according to the current game state
        """
        surface = pygame.Surface((self.sprite_w, self.sprite_h))
        if game_state == GameState.GAME_OVER:
            surface.blit(self.sprites["dead"], (0, 0))
        elif game_state == GameState.WIN:
            surface.blit(self.sprites["win"], (0, 0))
        elif game_state == GameState.MOUSE_DOWN and pressed:
            surface.blit(self.sprites["pressed"], (0, 0))
        elif game_state == GameState.MOUSE_DOWN:
            surface.blit(self.sprites["supprise"], (0, 0))
        else:
            surface.blit(self.sprites["smile"], (0, 0))
        return surface
