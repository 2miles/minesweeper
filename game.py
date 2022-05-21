import pygame
import vars
import my_utils

from gamestate import GameState
from grid import Grid
from status import Status, Faces
from background import Background
from debug import debug


# Create funtion to draw texts


class Game:
    def __init__(self, cols, rows, mines) -> None:
        pygame.init()
        self.cols = cols
        self.rows = rows
        self.mines = mines
        self.width = cols * vars.BOX_SIZE + vars.BORDER * 2
        self.height = rows * vars.BOX_SIZE + vars.TOP_AREA + vars.BORDER * 3
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()  # create timer

    def new_game(self):
        """
        Instantiates game objects and initializes time, score, gameState,
        then starts the game loop
        """
        self.ticks = 0
        self.face_pressed = False
        self.game_state = GameState.PLAYING
        self.background = Background(self.cols, self.rows)
        self.grid = Grid(self.rows, self.cols, self.mines)
        self.timer = Status(self.width - vars.BORDER * 2 - 64, vars.COUNTER_LOC)
        self.remaining = Status(vars.COUNTER_LOC, vars.COUNTER_LOC)
        self.faces = Faces(self.width // 2 - vars.FACE_W, vars.FACE_LOC_Y)
        self.game_loop()

    def game_loop(self):
        """
        Main game loop. Manages game clock, updates numerical displays, checks events,
        checks for win, updates display
        """
        while self.game_state != GameState.EXIT:
            # Reset screen
            self.clock.tick(60)  # Tick fps
            if self.game_state == GameState.PLAYING:
                self.timer.update_time()
            self.remaining.update(self.grid.mines_left)
            self.faces.update(self.grid.rect)
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
            if event.type == pygame.QUIT:
                self.game_state = GameState.EXIT
            if self.faces.pressed:
                self.new_game()
                break
            else:
                if (
                    event.type == pygame.MOUSEBUTTONUP
                    and self.game_state != GameState.GAME_OVER
                ):
                    self.game_state = GameState.PLAYING
                    for line in self.grid.boxes:
                        for box in line:
                            if box.rect.collidepoint(event.pos):
                                if event.button == 1 and event.button == 3:
                                    if self.grid.check_neighbors_for_flags(
                                        box.x, box.y
                                    ):
                                        if self.grid.reveal_grid(box.x, box.y):
                                            self.game_state = GameState.GAME_OVER
                                elif event.button == 1:  # Left click
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
        if self.grid.reveal_grid(box.x, box.y):
            self.game_state = GameState.GAME_OVER
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

        def draw_win_message():
            """
            Draws win message over the center of the screen when player wins
            """
            center_x = self.width / 2
            center_y = self.height / 2
            my_utils.draw_centered_text(
                self.display, "You Win!", 50, center_x, center_y
            )
            my_utils.draw_centered_text(
                self.display, f"Score: {self.final_score}", 40, center_x, center_y + 50
            )

        def draw_game_over_message():
            """
            Draws game over message over the center of the screen when player loses
            """
            center_x = self.width / 2
            center_y = self.height / 2
            my_utils.draw_centered_text(
                self.display, "Game Over", 50, center_x, center_y
            )

        self.display.blit(self.background.draw(), (0, 0))
        self.display.blit(
            self.faces.draw(self.game_state),
            (self.faces.rect),
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
        if vars.debug:
            debug(self.game_state, 0)
            debug(self.grid.mines_left, 40)
            debug(pygame.mouse.get_pos(), 80)
            debug(pygame.mouse.get_pressed(), 120)
