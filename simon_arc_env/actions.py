from typing import Dict
from enum import Enum
import pygame

class Actions(Enum):
    NEXT_PAGE = 0
    SUBMIT_DRAWING = 1
    SET_PIXEL = 2
    MOVE_UP = 3
    MOVE_DOWN = 4
    MOVE_LEFT = 5
    MOVE_RIGHT = 6
    DECREMENT_COLOR = 7
    INCREMENT_COLOR = 8
    ADJUST_CANVAS_SIZE = 9

    @classmethod
    def number_of_actions(cls) -> int:
        return 10
    
    @classmethod
    def keys_to_action(cls) -> Dict[int, int]:
        return {
            pygame.K_TAB: Actions.NEXT_PAGE.value,
            pygame.K_RETURN: Actions.SUBMIT_DRAWING.value,
            pygame.K_SPACE: Actions.SET_PIXEL.value,
            pygame.K_UP: Actions.MOVE_UP.value,
            pygame.K_DOWN: Actions.MOVE_DOWN.value,
            pygame.K_LEFT: Actions.MOVE_LEFT.value,
            pygame.K_RIGHT: Actions.MOVE_RIGHT.value,
            pygame.K_n: Actions.DECREMENT_COLOR.value,
            pygame.K_m: Actions.INCREMENT_COLOR.value,
            pygame.K_s: Actions.ADJUST_CANVAS_SIZE.value
        }
