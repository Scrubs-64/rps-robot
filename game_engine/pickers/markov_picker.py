import random
from collections import Counter

from common.moves import ALL_MOVES, counter_to
from game_engine.pickers.base import MovePicker


class MarkovPicker(MovePicker):
    """Predicts the player's next move from their LAST move.

    It looks through the history for every earlier time the player threw the
    same move as just now, and checks what they threw right after. Example:
    history = rock, paper, rock, paper, rock. The player just threw rock, and
    after rock they always threw paper, so the arm expects paper and plays scissors.
    """

    def __init__(self, min_history=4):
        self.min_history = min_history  # rounds to watch before trusting the pattern

    def choose_move(self, history):
        # Not enough data yet: play randomly
        if len(history) < self.min_history:
            return random.choice(ALL_MOVES)

        last_move = history[-1]

        # Count what the player threw right after `last_move` in earlier rounds.
        # zip(history, history[1:]) pairs each move with the move that followed it.
        followers = Counter()
        for before, after in zip(history, history[1:]):
            if before == last_move:
                followers[after] += 1

        # The player has never been in this situation before: play randomly
        if not followers:
            return random.choice(ALL_MOVES)

        # Most likely follow-ups; on a tie, pick one at random
        top_count = max(followers.values())
        likely = [move for move, n in followers.items() if n == top_count]
        predicted = random.choice(likely)

        return counter_to(predicted)
