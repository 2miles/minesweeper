from spritesheet import Spritesheet
import vars
import pygame


class Box:
    """
    Defines a single square of the game grid
    """

    def __init__(self, x, y, val):
        self.x = x
        self.y = y
        self.val = val  # Number of bombs next to box, -1 is mine
        self.rect = pygame.Rect(
            self.x * vars.BOX_SIZE + vars.GRID_LOC_X,
            self.y * vars.BOX_SIZE + vars.GRID_LOC_Y,
            vars.BOX_SIZE,
            vars.BOX_SIZE,
        )
        self.clicked = False  # Has box been clicked
        self.mineClicked = False  # Has box been clicked and its a mine
        self.mineFalse = False  # Has player flagged the wrong box without bomb
        self.flag = False  # Has player flagged the box
        self.sprites = Spritesheet.parse_box_sprites(Spritesheet)

    def draw(self):
        """
        Draws a Box with a specific sprite depending on its value and its
        boolean attributes mineFalse, clicked, mineClicked, and flag
        """
        mouse_pos = pygame.mouse.get_pos()
        surface = pygame.Surface((vars.BOX_SIZE, vars.BOX_SIZE))
        if self.mineFalse:
            surface.blit(self.sprites["box_no_bomb"], (0, 0))
        if (
            self.rect.collidepoint(mouse_pos)
            and self.clicked == False
            and pygame.mouse.get_pressed()[0]
        ):
            surface.blit(self.sprites["box_empty"], (0, 0))
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
