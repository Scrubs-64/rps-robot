"""Scoreboard: keeps track of the current score of one match.

Use it from another file:

    from scoreboard import Scoreboard

    board = Scoreboard(rounds_to_win=3)
    board.record("player")      # or "arm" or "draw"
    print(board)                # Player 1 - Arm 0 (draws: 0)
    board.winner()              # "player", "arm", or None while the match is still going
    board.reset()               # start a new match

Try it out by running this file directly:

    python scoreboard.py
"""

PLAYER = "player"
ARM = "arm"
DRAW = "draw"


class Scoreboard:
    def __init__(self, rounds_to_win=3):
        self.rounds_to_win = rounds_to_win
        self.reset()

    def reset(self):
        """Set all scores back to 0."""
        self.player_score = 0
        self.arm_score = 0
        self.draws = 0

    def record(self, result):
        """Add one round. result must be "player", "arm" or "draw"."""
        if result == PLAYER:
            self.player_score += 1
        elif result == ARM:
            self.arm_score += 1
        elif result == DRAW:
            self.draws += 1
        else:
            raise ValueError(f"Invalid result: {result}")

    def winner(self):
        """Return "player" or "arm" once someone reached rounds_to_win, otherwise None."""
        if self.player_score >= self.rounds_to_win:
            return PLAYER
        if self.arm_score >= self.rounds_to_win:
            return ARM
        return None

    def __str__(self):
        return f"Player {self.player_score} - Arm {self.arm_score} (draws: {self.draws})"


def main():
    """Small interactive test: type the result of each round and watch the score."""
    board = Scoreboard(rounds_to_win=3)
    print("First to 3 wins. Type p (player won), a (arm won), d (draw), r (reset), q (quit)")
    print(board)

    results = {"p": PLAYER, "a": ARM, "d": DRAW}
    while True:
        key = input("> ").strip().lower()
        if key == "q":
            break
        if key == "r":
            board.reset()
        elif key in results:
            board.record(results[key])
        else:
            print("Please type p, a, d, r or q")
            continue

        print(board)
        if board.winner():
            print(f"{board.winner()} wins the match! Starting a new one.")
            board.reset()


if __name__ == "__main__":
    main()