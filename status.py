from spritesheet import Spritesheet
import vars
import pygame


class Status:
    def __init__(self, x, y):
        self.num = 0
        self.sprite_w = 26
        self.sprite_h = 46
        self.rect = (x, y, self.sprite_w * 3, self.sprite_h)
        self.sprites = Spritesheet.parse_number_sprites(Spritesheet)

    def update(self, number):
        self.num = number

    def draw(self):
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
    def __init__(self, x, y):
        self.sprite_w = 52
        self.sprite_h = 52
        self.sprites = Spritesheet.parse_face_sprites(Spritesheet)

    def draw(self, game_state):
        """
        Draws the center face according to the current game state
        """
        surface = pygame.Surface((self.sprite_w, self.sprite_h))
        if game_state == "Game Over":
            surface.blit(self.sprites["face_dead"], (0, 0))
        elif game_state == "Win":
            surface.blit(self.sprites["face_win"], (0, 0))
        elif game_state == "Mouse down":
            surface.blit(self.sprites["face_supprise"], (0, 0))
        else:
            surface.blit(self.sprites["face_smile"], (0, 0))
        return surface

    class GameOverText:
        pass
