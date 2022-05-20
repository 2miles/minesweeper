from enum import Enum


class MenuState(Enum):
    """
    EXIT, RUNNING
    """

    EXIT = -1
    RUNNING = 1


class GameState(Enum):
    """
    EXIT, PLAYING, MOUSE_DOWN, WIN, GAME_OVER
    """

    EXIT = -1
    PLAYING = 1
    MOUSE_DOWN = 2
    WIN = 3
    GAME_OVER = 4
