from spritesheet import Spritesheet
import vars
import pygame


class Background:
    def __init__(self, cols, rows):
        self.sprites = Spritesheet.parse_border_sprites(Spritesheet)
        self.cols = cols
        self.rows = rows
        self.width = cols * vars.BOX_SIZE + vars.BORDER * 2
        self.height = rows * vars.BOX_SIZE + vars.TOP_AREA + vars.BORDER * 3
        self.inner_width = cols * vars.BOX_SIZE
        self.inner_height = rows * vars.BOX_SIZE

    def draw(self):
        """
        Draw the background by patching together sprites from border_sheet.png
        """
        surface = pygame.Surface((self.width, self.height))
        surface.fill(vars.BG_COLOR)

        for i in range(self.rows + 4):
            surface.blit(
                self.sprites["vertical_bar"], (self.inner_width + vars.BORDER, i * 32)
            )
            surface.blit(self.sprites["vertical_bar"], (0, i * 32))
        for i in range(self.cols + 2):
            surface.blit(self.sprites["horizontal_bar"], (i * 32, 0))
            surface.blit(
                self.sprites["horizontal_bar"], (i * 32, vars.BORDER + vars.TOP_AREA)
            )
            surface.blit(
                self.sprites["horizontal_bar"],
                (i * 32, vars.GRID_LOC_Y + self.inner_height),
            )
        surface.blit(self.sprites["top_left"], (0, 0))
        surface.blit(self.sprites["top_right"], (self.inner_width + vars.BORDER, 0))
        surface.blit(
            self.sprites["bottom_left"], (0, self.inner_height + vars.GRID_LOC_Y)
        )
        surface.blit(
            self.sprites["bottom_right"],
            (self.inner_width + vars.BORDER, self.height - vars.BORDER),
        )
        surface.blit(self.sprites["left_t"], (0, vars.TOP_AREA + vars.BORDER))
        surface.blit(
            self.sprites["right_t"],
            (self.inner_width + vars.BORDER, vars.TOP_AREA + vars.BORDER),
        )
        return surface
