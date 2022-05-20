import vars
import pygame
from game import Game
from background import Background
from gamestate import MenuState
import my_utils


class Menu:
    def __init__(self) -> None:
        pygame.init()
        self.width = vars.MENU_WIDTH
        self.height = vars.MENU_HEIGHT
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Minesweeper Menu")
        self.clock = pygame.time.Clock()
        self.background = Background(vars.MENU_COLS, vars.MENU_ROWS)
        self.menu_state = MenuState.RUNNING

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    game = Game(cols=9, rows=9, mines=10)
                    game.new_game()
                    self.display = pygame.display.set_mode((self.width, self.height))
                elif event.key == pygame.K_i:
                    game = Game(cols=16, rows=16, mines=40)
                    game.new_game()
                    self.display = pygame.display.set_mode((self.width, self.height))
                elif event.key == pygame.K_e:
                    game = Game(cols=30, rows=16, mines=1)
                    game.new_game()
                    self.display = pygame.display.set_mode((self.width, self.height))

    def draw(self):
        self.display.blit(self.background.draw(), (0, 0))
        my_utils.draw_centered_text(self.display, "MINESWEEPER", 40, self.width / 2, 52)
        my_utils.draw_centered_text(
            self.display, "B --  Beginner      ", 30, self.width / 2, 140
        )
        my_utils.draw_centered_text(
            self.display, "I  --  Intermediate", 30, self.width / 2, 200
        )
        my_utils.draw_centered_text(
            self.display, "E --  Expert           ", 30, self.width / 2, 260
        )


def main():
    menu = Menu()
    menu.menu_loop()
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
