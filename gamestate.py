from enum import Enum


class GameState(Enum):
    EXIT = -1
    PLAYING = 1
    MOUSE_DOWN = 2
    WIN = 3
    GAME_OVER = 4
