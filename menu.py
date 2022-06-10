import pygame
import vars
import my_utils
from game import Game
from background import Background
from gamestate import MenuState
from button import Button


class Menu:
    def __init__(self) -> None:
        pygame.init()
        self.width = vars.MENU_WIDTH
        self.height = vars.MENU_HEIGHT
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Minesweeper Menu")
        self.clock = pygame.time.Clock()
        self.menu_state = MenuState.RUNNING
        self.background = Background(vars.MENU_COLS, vars.MENU_ROWS)
        self.buttons = {}
        self.buttons["beginner"] = Button(self.width / 2, 150, "Beginner")
        self.buttons["intermediate"] = Button(self.width / 2, 200, "Intermediate")
        self.buttons["expert"] = Button(self.width / 2, 250, "Expert")
        self.buttons["scores"] = Button(self.width / 2, 320, "High Scores")

    def menu_loop(self):
        while self.menu_state != MenuState.EXIT:
            self.clock.tick(60)
            for button in self.buttons.values():
                button.update()
            self.check_events()
            self.draw()
            pygame.display.update()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.menu_state = MenuState.EXIT
            if self.buttons["beginner"].clicked:
                self.new_game_window(9, 9, 10)
            elif self.buttons["intermediate"].clicked:
                self.new_game_window(16, 16, 40)
            elif self.buttons["expert"].clicked:
                self.new_game_window(30, 16, 100)

    def new_game_window(self, cols, rows, mines):
        game = Game(cols, rows, mines)
        game.new_game()
        self.display = pygame.display.set_mode((self.width, self.height))
        for button in self.buttons.values():
            button.clicked = False

    def draw(self):
        self.display.blit(self.background.draw(), (0, 0))
        my_utils.draw_centered_text(self.display, "MINESWEEPER", 40, self.width / 2, 52)
        self.display.blit(
            self.buttons["beginner"].draw(), (self.buttons["beginner"].rect)
        )
        self.display.blit(
            self.buttons["intermediate"].draw(), (self.buttons["intermediate"].rect)
        )
        self.display.blit(self.buttons["expert"].draw(), (self.buttons["expert"].rect))
        self.display.blit(self.buttons["scores"].draw(), (self.buttons["scores"].rect))
