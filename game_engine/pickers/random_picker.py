import random

from common.moves import ALL_MOVES
from game_engine.pickers.base import MovePicker


class RandomPicker(MovePicker):
    def choose_move(self, history):
        return random.choice(ALL_MOVES)