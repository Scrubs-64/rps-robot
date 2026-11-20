"""Playable Rock Paper Scissors game in the terminal.

You type your move, and a fake arm prints what it would do.
The game engine, scoreboard and picker are the real ones.

Run it from the project root (venv active):

    python -m tests.keyboard_game
    python -m tests.keyboard_game --mode adaptive --rounds 5
"""
import argparse
import sys
from pathlib import Path

# Make the project root importable even when this file is run directly from tests/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from arm_controller import MockArm
from game_engine import GameEngine, Scoreboard
from game_engine.pickers import make_picker

KEYS = {"r": "rock", "p": "paper", "s": "scissors"}

RESULT_TEXT = {
    "player": "You win this round!",
    "arm": "The arm wins this round.",
    "draw": "It's a draw.",
}


class KeyboardPlayer:
    """Stands in for the camera: the player types their move.

    Has the same read_gesture() method as the real vision module, so the engine
    cannot tell the difference.
    """

    def read_gesture(self):
        text = input("Your move (r = rock, p = paper, s = scissors, q = quit): ").strip().lower()
        if text == "q":
            raise KeyboardInterrupt        # handled in main(); ends the program
        return KEYS.get(text)              # anything else counts as "no gesture detected"


def play_match(mode, rounds_to_win):
    board = Scoreboard(rounds_to_win)
    engine = GameEngine(
        arm=MockArm(),
        vision=KeyboardPlayer(),
        picker=make_picker(mode),
        scoreboard=board,
    )
    engine.start_game()
    print(f"\nFirst to {rounds_to_win} wins. Opponent mode: {mode}\n")

    rounds_played = 0
    status = engine.get_status()
    while status["state"] == "READY":
        print(f"--- Round {rounds_played + 1} ---")
        engine.play_round()
        status = engine.get_status()

        if status["state"] == "ERROR":
            print(f"Something went wrong: {status['error']}")
            return

        if status["last_result"] is None:      # round was cancelled, nothing scored
            print(status["error"])
            print()
            continue

        rounds_played += 1
        print(f"You: {status['last_player_move']}   Arm: {status['last_arm_move']}")
        print(RESULT_TEXT[status["last_result"]])
        print(f"Score: You {status['player_score']} - Arm {status['arm_score']} "
              f"(draws: {status['draws']})\n")

    if board.match_winner() == "player":
        print("You won the match!")
    else:
        print("The arm won the match.")


def main():
    parser = argparse.ArgumentParser(description="Play Rock Paper Scissors in the terminal")
    parser.add_argument("--mode", default="random", choices=["random", "frequency", "adaptive"],
                        help="how the arm picks its moves (default: random)")
    parser.add_argument("--rounds", type=int, default=3,
                        help="rounds needed to win the match (default: 3)")
    args = parser.parse_args()

    try:
        while True:
            play_match(args.mode, args.rounds)
            if input("\nPlay again? (y/n): ").strip().lower() != "y":
                break
    except KeyboardInterrupt:                  # q, or Ctrl+C
        pass
    print("\nBye!")


if __name__ == "__main__":
    main()
