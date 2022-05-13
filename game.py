import pygame
import vars

from grid import Grid
from status import Status, Faces
from background import Background
from debug import debug


# Create funtion to draw texts

pygame.init()
display = pygame.display.set_mode((vars.SCREEN_W, vars.SCREEN_H))  # Create display
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()  # create timer


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
    final_score = 0

    background = Background()
    grid = Grid(vars.ROWS, vars.COLS, vars.MINES)
    timer = Status(vars.TIMER_LOC_X, vars.TIMER_LOC_Y)
    remaining = Status(vars.TIMER_LOC_Y, vars.TIMER_LOC_Y)
    faces = Faces(vars.FACE_LOC_X, vars.FACE_LOC_Y)

    while gameState != "Exit":
        # Reset screen
        clock.tick(60)  # Tick fps
        seconds += 1
        if seconds % 60 == 0:
            if gameState == "Playing":
                timer.update(seconds // 60)
                final_score = seconds // 60
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    gameState = "Mouse down"
                elif event.type == pygame.MOUSEBUTTONUP:
                    gameState = "Playing"
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
        if gameState != "Exit":
            if grid.check_for_win():
                gameState = "Win"

        # render stuff to the screen
        display.blit(background.draw(), (0, 0))
        display.blit(faces.draw(gameState), (vars.FACE_LOC_X, vars.FACE_LOC_Y))
        display.blit(timer.draw(), (timer.rect))
        display.blit(remaining.draw(), (remaining.rect))
        display.blit(grid.draw(), (grid.rect))
        if gameState == "Win":
            display.blit(drawText("You Won!", 50), (vars.BORDER, vars.SCREEN_H // 2))
            display.blit(
                drawText(f"Your Score is {final_score}", 50),
                (vars.BORDER, vars.SCREEN_H // 2 + 50),
            )
            display.blit(
                drawText("R to restart", 50),
                (vars.BORDER, vars.SCREEN_H // 2 + 100),
            )
        if gameState == "Game Over":
            display.blit(
                drawText("Game over!", 50), (vars.SCREEN_W // 2, vars.SCREEN_H // 2)
            )
            display.blit(
                drawText("R to restart", 50),
                (vars.SCREEN_W // 2, vars.SCREEN_H // 2 + 50),
            )

        if vars.DEBUG:
            debug(gameState, 0)
            debug(grid.mines_left, 40)
            debug(pygame.mouse.get_pos(), 80)
            debug(pygame.mouse.get_pressed(), 120)

        # update screen
        pygame.display.update()


gameLoop()
pygame.quit()
quit()
