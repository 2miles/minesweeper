from box import Box
import vars
import pygame
import random


class Grid:
    boxes = []
    mines = []

    def __init__(self, rows, cols, num_mines):
        self.rows = rows
        self.cols = cols
        self.width = self.cols * vars.BOX_SIZE
        self.height = self.rows * vars.BOX_SIZE
        self.num_mines = num_mines
        self.mines_left = num_mines
        self.mines = self.generate_mines()
        self.generate_boxes()
        self.populate_values()
        self.rect = (vars.GRID_LOC_X, vars.GRID_LOC_Y, self.width, self.height)

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
        for _ in range(self.num_mines - 1):
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

    def revealGrid(self, x, y):
        """
        Sets the box at argument coords clicked attribute to True.
        If its not a mine, recursivly call revealGrid() on all adjacent boxes
        that are not mines.
        If it is a mine, reveal all mines.
        """
        self.boxes[y][x].clicked = True
        if self.boxes[y][x].val == 0:
            for j in range(-1, 2):
                if x + j >= 0 and x + j < self.cols:
                    for i in range(-1, 2):
                        if y + i >= 0 and y + i < self.rows:
                            if not self.boxes[y + i][x + j].clicked:
                                self.revealGrid(x + j, y + i)
        # If you click on a mine reveal all the mines
        elif self.boxes[y][x].val == -1:
            for m in self.mines:
                if not self.boxes[m[1]][m[0]].clicked:
                    self.revealGrid(m[0], m[1])

    def draw(self):
        surface = pygame.Surface((self.width, self.height))
        for line in Grid.boxes:
            for box in line:
                surface.blit(box.draw(), (box.x * vars.BOX_SIZE, box.y * vars.BOX_SIZE))
        return surface
