import pygame
import vars

from spritesheet import Spritesheet
from grid import Grid
from debug import debug

# Create funtion to draw texts

pygame.init()
display = pygame.display.set_mode((vars.SCREEN_W, vars.SCREEN_H))  # Create display
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()  # create timer

borders = Spritesheet.parse_border_sprites(Spritesheet)
faces = Spritesheet.parse_face_sprites(Spritesheet)


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


def draw_face(game_state):
    """
    Draws the center face according to the current game state
    """
    surface = pygame.Surface((52, 52))
    if game_state == "Game Over":
        surface.blit(faces["face_dead"], (0, 0))
    elif game_state == "Win":
        surface.blit(faces["face_win"], (0, 0))
    elif game_state == "Mouse down":
        surface.blit(faces["face_supprise"], (0, 0))
    else:
        surface.blit(faces["face_smile"], (0, 0))
    return surface


def draw_background(game_state):
    """
    Draw the background by patching together sprites from border_sheet.png
    """
    surface = pygame.Surface((vars.SCREEN_W, vars.SCREEN_H))
    surface.fill(vars.BG_COLOR)

    surface.blit(draw_face(game_state), (vars.FACE_LOC_X, vars.FACE_LOC_Y))

    for i in range(vars.ROWS + 4):
        surface.blit(borders["vertical_bar"], (vars.grid_w + vars.BORDER, i * 32))
        surface.blit(borders["vertical_bar"], (0, i * 32))
    for i in range(vars.COLS + 2):
        surface.blit(borders["horizontal_bar"], (i * 32, 0))
        surface.blit(borders["horizontal_bar"], (i * 32, vars.BORDER + vars.TOP_AREA))
        surface.blit(borders["horizontal_bar"], (i * 32, vars.GRID_LOC_Y + vars.grid_h))
    surface.blit(borders["top_left"], (0, 0))
    surface.blit(borders["top_right"], (vars.grid_w + vars.BORDER, 0))
    surface.blit(borders["bottom_left"], (0, vars.grid_h + vars.GRID_LOC_Y))
    surface.blit(
        borders["bottom_right"],
        (vars.grid_w + vars.BORDER, vars.SCREEN_H - vars.BORDER),
    )
    surface.blit(borders["left_t"], (0, vars.TOP_AREA + vars.BORDER))
    surface.blit(
        borders["right_t"], (vars.grid_w + vars.BORDER, vars.TOP_AREA + vars.BORDER)
    )
    return surface


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


def gameLoop():
    gameState = "Playing"  # Game state
    seconds = 0

    grid = Grid(vars.ROWS, vars.COLS, vars.MINES)
    timer = Status(vars.TIMER_LOC_X, vars.TIMER_LOC_Y)
    remaining = Status(vars.TIMER_LOC_Y, vars.TIMER_LOC_Y)

    while gameState != "Exit":
        # Reset screen
        clock.tick(60)  # Tick fps
        seconds += 1
        if seconds % 60 == 0:
            if gameState != "Win":
                timer.update(seconds // 60)
        remaining.update(grid.mines_left)

        for event in pygame.event.get():
            # Check if player close window
            if event.type == pygame.QUIT:
                gameState = "Exit"

            # If game is over, user can press 'r' to restart
            if gameState == "Game Over" or gameState == "Win":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        gameState = "Exit"
                        gameLoop()
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    for line in grid.boxes:
                        for box in line:
                            if box.rect.collidepoint(event.pos):
                                if event.button == 1:
                                    # If player left clicked on the box
                                    grid.revealGrid(box.x, box.y)
                                    # Toggle flag off
                                    if box.flag:
                                        grid.mines_left += 1
                                        box.flag = False
                                    # If it's a mine
                                    if box.val == -1:
                                        gameState = "Game Over"
                                        box.mineClicked = True
                                elif event.button == 3:
                                    # If the player right clicked
                                    if not box.clicked:
                                        if box.flag:
                                            box.flag = False
                                            grid.mines_left += 1
                                        else:
                                            box.flag = True
                                            grid.mines_left -= 1

        # check for win
        finished = True
        for line in grid.boxes:
            for box in line:
                if box.val != -1 and not box.clicked:
                    finished = False
        if finished and gameState != "Exit":
            if grid.mines_left == 0:
                gameState = "Win"

        display.blit(draw_background(gameState), (0, 0))
        display.blit(timer.draw(), (timer.rect))
        display.blit(remaining.draw(), (remaining.rect))
        display.blit(grid.draw(), (grid.rect))
        if gameState == "Win":
            display.blit(
                drawText("You Won!", 50), (vars.SCREEN_W // 2, vars.SCREEN_H // 2)
            )
            display.blit(
                drawText("R to restart", 50),
                (vars.SCREEN_W // 2, vars.SCREEN_H // 2 + 50),
            )
        if gameState == "Game Over":
            display.blit(
                drawText("Game over!", 50), (vars.SCREEN_W // 2, vars.SCREEN_H // 2)
            )
            display.blit(
                drawText("R to restart", 50),
                (vars.SCREEN_W // 2, vars.SCREEN_H // 2 + 50),
            )

        debug(pygame.mouse.get_pos())
        debug(pygame.mouse.get_pressed(), 40)
        debug(gameState, 80)
        debug(grid.mines_left, 120)
        # debug("mouse", pygame.mouse.get_pos()[1], pygame.mouse.get_pos()[0])

        pygame.display.update()  # Update screen


gameLoop()
pygame.quit()
quit()
