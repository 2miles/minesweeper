import pygame


def drawText(txt, size):
    """
    Returns a surface with the given text. The text is on a black grey background
    """
    screen_text = pygame.font.SysFont("Calibri", size, True).render(
        txt, True, (0, 0, 0)
    )
    rect = screen_text.get_rect()
    surface = pygame.Surface((rect.width, rect.height))
    surface.fill((192, 192, 192))
    surface.blit(screen_text, (0, 0))
    return surface


def draw_centered_text(surf, text, size, x, y):
    """
    Draws text on surf centered around x,y
    """
    text = drawText(text, size)
    text_rect = text.get_rect()
    surf.blit(
        text,
        (
            x - text_rect.centerx,
            y - text_rect.centery,
        ),
    )
