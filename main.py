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
        self.beginner_button = Button(self.width / 2, 150, "Beginner")
        self.intermediate_button = Button(self.width / 2, 200, "Intermediate")
        self.expert_button = Button(self.width / 2, 250, "Expert")

    def menu_loop(self):
        while self.menu_state != MenuState.EXIT:
            self.clock.tick(60)
            self.check_events()
            self.draw()
            pygame.display.update()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.menu_state = MenuState.EXIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.beginner_button.rect.collidepoint(event.pos):
                    if event.button == 1:
                        self.beginner_button.is_pressed = True
                if self.intermediate_button.rect.collidepoint(event.pos):
                    if event.button == 1:
                        self.intermediate_button.is_pressed = True
                if self.expert_button.rect.collidepoint(event.pos):
                    if event.button == 1:
                        self.expert_button.is_pressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.beginner_button.is_pressed = False
                self.intermediate_button.is_pressed = False
                self.expert_button.is_pressed = False
                if self.beginner_button.rect.collidepoint(event.pos):
                    game = Game(cols=9, rows=9, mines=10)
                    game.new_game()
                    self.display = pygame.display.set_mode((self.width, self.height))
                elif self.intermediate_button.rect.collidepoint(event.pos):
                    game = Game(cols=16, rows=16, mines=40)
                    game.new_game()
                    self.display = pygame.display.set_mode((self.width, self.height))
                elif self.expert_button.rect.collidepoint(event.pos):
                    game = Game(cols=30, rows=16, mines=100)
                    game.new_game()
                    self.display = pygame.display.set_mode((self.width, self.height))

    def draw(self):
        self.display.blit(self.background.draw(), (0, 0))
        my_utils.draw_centered_text(self.display, "MINESWEEPER", 40, self.width / 2, 52)
        self.display.blit(self.beginner_button.draw(), (self.beginner_button.rect))
        self.display.blit(
            self.intermediate_button.draw(), (self.intermediate_button.rect)
        )
        self.display.blit(self.expert_button.draw(), (self.expert_button.rect))


def main():
    menu = Menu()
    menu.menu_loop()
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
