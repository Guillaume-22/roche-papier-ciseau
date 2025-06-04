from enum import Enum


class GameState(Enum):
    NOT_STARTED = 0
    ROUND_DONE = 1
    GAME_OVER = 2
    ROUND_ACTIVE = 3
