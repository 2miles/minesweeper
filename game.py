import pygame
import random

from spritesheet import Spritesheet

pygame.init()

BG_COLOR = (192, 192, 192)
BOX_SIZE = 32
BORDER = 22
TOP_AREA = BOX_SIZE * 2
GRID_X = BORDER
GRID_Y = TOP_AREA + BORDER * 2

game_w = 20  # number of boxes per row of grid
game_h = 10  # number of boxes per column of grid
num_mines = 20

grid_w = game_w * BOX_SIZE
grid_h = game_h * BOX_SIZE
display_width = grid_w + BORDER * 2  # Display width
display_height = grid_h + TOP_AREA + BORDER * 3  # Display height


display = pygame.display.set_mode((display_width, display_height))  # Create display
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()  # create timer


borders = Spritesheet.parse_border_sprites(Spritesheet)


class Box:
    def __init__(self, x, y, val):
        self.x = x
        self.y = y
        self.val = val  # Number of bombs next to box, -1 is mine
        self.rect = pygame.Rect(
            self.x * BOX_SIZE + BORDER,
            self.y * BOX_SIZE + TOP_AREA + BORDER * 2,
            BOX_SIZE,
            BOX_SIZE,
        )
        self.sprites = Spritesheet.parse_box_sprites(Spritesheet)
        self.clicked = False  # Has box been clicked
        self.mineClicked = False  # Has box been clicked and its a mine
        self.mineFalse = False  # Has player flagged the wrong box without bomb
        self.flag = False  # Has player flagged the box

    def draw(self):
        """
        Draws a Box with a specific sprite depending on its value and its
        boolean attributes mineFalse, clicked, mineClicked, and flag
        """
        surface = pygame.Surface((BOX_SIZE, BOX_SIZE))
        if self.mineFalse:
            surface.blit(self.sprites["box_no_bomb"], (0, 0))
        else:
            if self.clicked:
                if self.val == -1:
                    if self.mineClicked:
                        surface.blit(self.sprites["box_red_bomb"], (0, 0))
                    else:
                        surface.blit(self.sprites["box_bomb"], (0, 0))
                else:
                    if self.val == 0:
                        surface.blit(self.sprites["box_empty"], (0, 0))
                    elif self.val == 1:
                        surface.blit(self.sprites["box_1"], (0, 0))
                    elif self.val == 2:
                        surface.blit(self.sprites["box_2"], (0, 0))
                    elif self.val == 3:
                        surface.blit(self.sprites["box_3"], (0, 0))
                    elif self.val == 4:
                        surface.blit(self.sprites["box_4"], (0, 0))
                    elif self.val == 5:
                        surface.blit(self.sprites["box_5"], (0, 0))
                    elif self.val == 6:
                        surface.blit(self.sprites["box_6"], (0, 0))
                    elif self.val == 7:
                        surface.blit(self.sprites["box_7"], (0, 0))
                    elif self.val == 8:
                        surface.blit(self.sprites["box_8"], (0, 0))
            else:
                if self.flag:
                    surface.blit(self.sprites["box_flag"], (0, 0))
                else:
                    surface.blit(self.sprites["box_full"], (0, 0))
        return surface


class Grid:
    boxes = []
    mines = []

    def __init__(self):
        self.rows = game_h
        self.cols = game_w
        self.width = self.cols * BOX_SIZE
        self.height = self.rows * BOX_SIZE
        self.mines = self.generate_mines()
        self.generate_boxes()
        self.populate_values()
        self.rect = (BORDER, TOP_AREA + BORDER * 2, self.width, self.height)
        self.mines_left = num_mines

    def generate_boxes(self):
        for j in range(self.rows):
            line = []
            for i in range(self.cols):
                if [i, j] in self.mines:
                    line.append(Box(i, j, -1))
                else:
                    line.append(Box(i, j, 0))
            self.boxes.append(line)

    def generate_mines(self):
        mines = [[random.randrange(0, self.cols), random.randrange(0, self.rows)]]
        for _ in range(num_mines - 1):
            pos = [random.randrange(0, self.cols), random.randrange(0, self.rows)]
            complete = False
            while not complete:
                for i in range(len(mines)):
                    if pos == mines[i]:
                        pos = [
                            random.randrange(0, self.cols),
                            random.randrange(0, self.rows),
                        ]
                        break
                    if i == len(mines) - 1:
                        complete = True
            mines.append(pos)
        return mines

    def populate_values(self):
        """
        Iterate through each Box in the Grid. For each Box that is not a bomb,
        increment it's value for every bomb that is adjacent to it.
        """
        for lines in self.boxes:
            for box in lines:
                if box.val != -1:
                    for j in range(-1, 2):
                        if box.x + j >= 0 and box.x + j < self.cols:
                            for i in range(-1, 2):
                                if box.y + i >= 0 and box.y + i < self.rows:
                                    if self.boxes[box.y + i][box.x + j].val == -1:
                                        box.val += 1

    def revealGrid(self, box_x, box_y):
        """
        Sets the box at argument coords clicked attribute to True.
        If its not a mine, recursivly call revealGrid() on all adjacent boxes
        that are not mines.
        If it is a mine, reveal all mines.
        """
        self.boxes[box_y][box_x].clicked = True
        if self.boxes[box_y][box_x].val == 0:
            for j in range(-1, 2):
                if box_x + j >= 0 and box_x + j < game_w:
                    for i in range(-1, 2):
                        if box_y + i >= 0 and box_y + i < game_h:
                            if not self.boxes[box_y + i][box_x + j].clicked:
                                self.revealGrid(
                                    self.boxes[box_y + i][box_x + j].x,
                                    self.boxes[box_y + i][box_x + j].y,
                                )
        # If you click on a mine reveal all the mines
        elif self.boxes[box_y][box_x].val == -1:
            for m in self.mines:
                if not self.boxes[m[1]][m[0]].clicked:
                    self.revealGrid(self.boxes[m[1]][m[0]].x, self.boxes[m[1]][m[0]].y)

    def draw(self):
        surface = pygame.Surface((self.width, self.height))
        for line in Grid.boxes:
            for box in line:
                surface.blit(box.draw(), (box.x * BOX_SIZE, box.y * BOX_SIZE))
        return surface


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


def draw_background():
    """
    Draw the background by patching together the sprites from border_sheet.png
    """
    surface = pygame.Surface((display_width, display_height))
    surface.fill(BG_COLOR)
    surface.blit(borders["top_left"], (0, 0))
    surface.blit(borders["top_right"], (grid_w + BORDER, 0))
    surface.blit(borders["bottom_left"], (0, grid_h + GRID_Y))
    surface.blit(borders["bottom_right"], (grid_w + 22, grid_h + GRID_Y))
    surface.blit(borders["left_t"], (0, TOP_AREA + BORDER))
    surface.blit(borders["right_t"], (grid_w + BORDER, TOP_AREA + BORDER))
    for i in range(2):
        surface.blit(borders["vertical_bar"], (0, BORDER + i * 32))
        surface.blit(borders["vertical_bar"], (grid_w + BORDER, BORDER + i * 32))
    for i in range(game_h):
        surface.blit(
            borders["vertical_bar"],
            (grid_w + BORDER, GRID_Y + i * 32),
        )
        surface.blit(borders["vertical_bar"], (0, GRID_Y + i * 32))
    for i in range(game_w):
        surface.blit(borders["horizontal_bar"], (BORDER + i * 32, 0))
        surface.blit(borders["horizontal_bar"], (BORDER + i * 32, BORDER + TOP_AREA))
        surface.blit(
            borders["horizontal_bar"],
            (BORDER + i * 32, GRID_Y + game_h * 32),
        )
    return surface


def gameLoop():
    gameState = "Playing"  # Game state
    seconds = 0
    score = 0

    grid = Grid()
    score = Status(grid_w - 64, BORDER + 6)
    timer = Status(BORDER + 6, BORDER + 6)

    while gameState != "Exit":
        # Reset screen
        clock.tick(60)  # Tick fps
        seconds += 1
        if seconds % 60 == 0:
            timer.update(seconds // 60)

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

        display.blit(draw_background(), (0, 0))
        display.blit(timer.draw(), (timer.rect))
        display.blit(score.draw(), (score.rect))
        display.blit(grid.draw(), (grid.rect))
        pygame.display.update()  # Update screen


gameLoop()
pygame.quit()
quit()
