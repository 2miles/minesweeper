from spritesheet import Spritesheet
import vars
import pygame


class Background:
    def __init__(self):
        self.sprites = Spritesheet.parse_border_sprites(Spritesheet)

    def draw(self):
        """
        Draw the background by patching together sprites from border_sheet.png
        """
        surface = pygame.Surface((vars.SCREEN_W, vars.SCREEN_H))
        surface.fill(vars.BG_COLOR)

        for i in range(vars.ROWS + 4):
            surface.blit(
                self.sprites["vertical_bar"], (vars.grid_w + vars.BORDER, i * 32)
            )
            surface.blit(self.sprites["vertical_bar"], (0, i * 32))
        for i in range(vars.COLS + 2):
            surface.blit(self.sprites["horizontal_bar"], (i * 32, 0))
            surface.blit(
                self.sprites["horizontal_bar"], (i * 32, vars.BORDER + vars.TOP_AREA)
            )
            surface.blit(
                self.sprites["horizontal_bar"], (i * 32, vars.GRID_LOC_Y + vars.grid_h)
            )
        surface.blit(self.sprites["top_left"], (0, 0))
        surface.blit(self.sprites["top_right"], (vars.grid_w + vars.BORDER, 0))
        surface.blit(self.sprites["bottom_left"], (0, vars.grid_h + vars.GRID_LOC_Y))
        surface.blit(
            self.sprites["bottom_right"],
            (vars.grid_w + vars.BORDER, vars.SCREEN_H - vars.BORDER),
        )
        surface.blit(self.sprites["left_t"], (0, vars.TOP_AREA + vars.BORDER))
        surface.blit(
            self.sprites["right_t"],
            (vars.grid_w + vars.BORDER, vars.TOP_AREA + vars.BORDER),
        )
        return surface
