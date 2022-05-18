import pygame
import vars
from enum import Enum

from grid import Grid
from status import Status, Faces
from background import Background
from debug import debug


# Create funtion to draw texts
def drawText(txt, s):
    screen_text = pygame.font.SysFont("Calibri", s, True).render(
        txt, True, (255, 255, 255)
    )
    rect = screen_text.get_rect()
    surface = pygame.Surface((rect.width, rect.height))
    surface.fill((100, 100, 100))
    surface.blit(screen_text, (0, 0))
    return surface


class GameState(Enum):
    EXIT = -1
    PLAYING = 1
    MOUSE_DOWN = 2
    WIN = 3
    GAME_OVER = 4


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display = pygame.display.set_mode(
            (vars.SCREEN_W, vars.SCREEN_H)
        )  # Create display
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()  # create timer

    def new_game(self):

        self.seconds = 0
        self.final_score = 0
        self.game_state = GameState.PLAYING

        self.background = Background()
        self.grid = Grid(vars.ROWS, vars.COLS, vars.MINES)
        self.timer = Status(vars.TIMER_LOC_X, vars.TIMER_LOC_Y)
        self.remaining = Status(vars.TIMER_LOC_Y, vars.TIMER_LOC_Y)
        self.faces = Faces(vars.FACE_LOC_X, vars.FACE_LOC_Y)
        self.game_loop()

    def game_loop(self):
        while self.game_state != GameState.EXIT:
            # Reset screen
            self.clock.tick(60)  # Tick fps
            self.seconds += 1
            if self.seconds % 60 == 0:
                if self.game_state == GameState.PLAYING:
                    self.timer.update(self.seconds // 60)
                    self.final_score = self.seconds // 60
            self.remaining.update(self.grid.mines_left)

            self.check_events()
            self.check_for_win()

            # render stuff to the screen
            self.display.blit(self.background.draw(), (0, 0))
            self.display.blit(
                self.faces.draw(self.game_state), (vars.FACE_LOC_X, vars.FACE_LOC_Y)
            )
            self.display.blit(self.timer.draw(), (self.timer.rect))
            self.display.blit(self.remaining.draw(), (self.remaining.rect))
            self.display.blit(self.grid.draw(), (self.grid.rect))

            if self.game_state == GameState.WIN:
                self.display.blit(
                    drawText("You Won!", 50), (vars.BORDER, vars.SCREEN_H // 2)
                )
                self.display.blit(
                    drawText(f"Your Score is {self.final_score}", 50),
                    (vars.BORDER, vars.SCREEN_H // 2 + 50),
                )
                self.display.blit(
                    drawText("R to restart", 50),
                    (vars.BORDER, vars.SCREEN_H // 2 + 100),
                )
            if self.game_state == GameState.GAME_OVER:
                self.display.blit(
                    drawText("Game over!", 50), (vars.SCREEN_W // 2, vars.SCREEN_H // 2)
                )
                self.display.blit(
                    drawText("R to restart", 50),
                    (vars.SCREEN_W // 2, vars.SCREEN_H // 2 + 50),
                )

            if vars.DEBUG:
                debug(self.game_state, 0)
                debug(self.grid.mines_left, 40)
                debug(pygame.mouse.get_pos(), 80)
                debug(pygame.mouse.get_pressed(), 120)

            # update screen
            pygame.display.update()

    def check_events(self):
        for event in pygame.event.get():
            # Check if player close window
            if event.type == pygame.QUIT:
                self.game_state = GameState.EXIT

            # If game is over, user can press 'r' to restart
            if (
                self.game_state == GameState.GAME_OVER
                or self.game_state == GameState.WIN
            ):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.game_state = GameState.EXIT
                        self.new_game()
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.game_state = GameState.MOUSE_DOWN
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.game_state = GameState.PLAYING
                    for line in self.grid.boxes:
                        for box in line:
                            if box.rect.collidepoint(event.pos):
                                if event.button == 1:
                                    # If player left clicked on the box
                                    self.grid.revealGrid(box.x, box.y)
                                    # Toggle flag off
                                    if box.flag:
                                        self.grid.mines_left += 1
                                        box.flag = False
                                    # If it's a mine
                                    if box.val == -1:
                                        self.game_state = GameState.GAME_OVER
                                        box.mineClicked = True
                                elif event.button == 3:
                                    # If the player right clicked
                                    if not box.clicked:
                                        if box.flag:
                                            box.flag = False
                                            self.grid.mines_left += 1
                                        else:
                                            box.flag = True
                                            self.grid.mines_left -= 1

    def check_for_win(self):

        if self.game_state != GameState.EXIT:
            if self.grid.check_for_win():
                self.game_state = GameState.WIN
