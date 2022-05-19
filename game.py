import pygame
import vars

from gamestate import GameState
from grid import Grid
from status import Status, Faces
from background import Background
from debug import debug


# Create funtion to draw texts


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display = pygame.display.set_mode(
            (vars.SCREEN_W, vars.SCREEN_H)
        )  # Create display
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()  # create timer

    def new_game(self):
        """
        Instantiates game objects and initializes time, score, gameState,
        then starts the game loop
        """
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
        """
        Main game loop. Manages game clock, updates numerical displays, checks events,
        checks for win, updates display
        """
        while self.game_state != GameState.EXIT:
            # Reset screen
            self.clock.tick(60)  # Tick fps
            self.seconds += 1
            if self.seconds % 60 == 0:
                if (
                    self.game_state == GameState.PLAYING
                    or self.game_state == GameState.MOUSE_DOWN
                ):
                    self.timer.update(self.seconds // 60)
                    self.final_score = self.seconds // 60
            self.remaining.update(self.grid.mines_left)
            self.check_events()
            self.check_for_win()
            self.draw()
            self.draw_debug_info()
            pygame.display.update()

    def check_events(self):
        """
        Processes events in the event queue.
        """
        for event in pygame.event.get():
            # Check if player close window
            if event.type == pygame.QUIT:
                self.game_state = GameState.EXIT
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
                                if event.button == 1:  # Left click
                                    self.reveal_box(box)
                                elif event.button == 3:  # right click
                                    self.toggle_flag(box)

    def toggle_flag(self, box):
        """
        Toggle flag of un-clicked box. If placing a flag then decrement mines left,
        else increment
        """
        if not box.clicked:
            if box.flag:
                box.flag = False
                self.grid.mines_left += 1
            else:
                box.flag = True
                self.grid.mines_left -= 1

    def reveal_box(self, box):
        """
        Reveal grid around box. If box if flagged and not a bomb then remove flag.
        If box is a bomb, regardless whether or not it is flagged, then game over.
        """
        self.grid.revealGrid(box.x, box.y)
        if box.flag:
            self.grid.mines_left += 1
            box.flag = False
        if box.val == -1:
            # left click on a mine
            self.game_state = GameState.GAME_OVER
            box.mineClicked = True

    def check_for_win(self):
        """
        Sets GameState to WIN if grid.check_for_win() return True
        """
        if self.game_state != GameState.EXIT:
            if self.grid.check_for_win():
                self.game_state = GameState.WIN

    def draw(self):
        """
        Draws all of the game elements on the screen.
        """

        def drawText(txt, size):
            """
            Returns a surface with the given text. The text is on an opaque grey background
            """
            screen_text = pygame.font.SysFont("Calibri", size, True).render(
                txt, True, (255, 255, 255)
            )
            rect = screen_text.get_rect()
            surface = pygame.Surface((rect.width, rect.height))
            surface.fill((100, 100, 100))
            surface.blit(screen_text, (0, 0))
            return surface

        def draw_win_message():
            """
            Draws message over the screen when player wins
            """
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

        def draw_game_over_message():
            """
            Draws message over screen when player loses
            """
            self.display.blit(
                drawText("Game over!", 50), (vars.SCREEN_W // 2, vars.SCREEN_H // 2)
            )
            self.display.blit(
                drawText("R to restart", 50),
                (vars.SCREEN_W // 2, vars.SCREEN_H // 2 + 50),
            )

        self.display.blit(self.background.draw(), (0, 0))
        self.display.blit(
            self.faces.draw(self.game_state), (vars.FACE_LOC_X, vars.FACE_LOC_Y)
        )
        self.display.blit(self.timer.draw(), (self.timer.rect))
        self.display.blit(self.remaining.draw(), (self.remaining.rect))
        self.display.blit(self.grid.draw(), (self.grid.rect))
        if self.game_state == GameState.WIN:
            draw_win_message()
        if self.game_state == GameState.GAME_OVER:
            draw_game_over_message()

    def draw_debug_info(self):
        """
        Draws debug info to the main display, if DEBUG is set to true
        """
        if vars.DEBUG:
            debug(self.game_state, 0)
            debug(self.grid.mines_left, 40)
            debug(pygame.mouse.get_pos(), 80)
            debug(pygame.mouse.get_pressed(), 120)
