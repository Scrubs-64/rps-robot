import random
from collections import Counter

from common.moves import ALL_MOVES, counter_to
from game_engine.pickers.base import MovePicker


class FrequencyPicker(MovePicker):
    """Predicts that the player will repeat their favorite move, and plays the move that beats it.

    Example: if the player's recent moves are rock, rock, paper, rock,
    the favorite is rock, so the arm plays paper.
    """

    def __init__(self, min_history=3, window=10):
        self.min_history = min_history
        self.window = window           
                                        # picker adapts if the player changes habits present only in the last moves

    def choose_move(self, history):
        # Not enough data yet => play randomly
        if len(history) < self.min_history:
            return random.choice(ALL_MOVES)

        recent = history[-self.window:]
        counts = Counter(recent)                  # e.g. {"rock": 3, "paper": 1}

        # Find the most common moves --- On a tie, pick one at random so the arm does not become predictable
        top_count = max(counts.values())
        favorites = [move for move, n in counts.items() if n == top_count]
        predicted = random.choice(favorites)

        return counter_to(predicted)
