"""Entry point: connects the arm, the camera, the game engine and the scoreboard, then plays.

Run it from the project root (venv active):

    python main.py --mock                       # fake arm, you type your move
    python main.py                              # real arm and real camera
    python main.py --mode adaptive --rounds 5   # harder opponent, first to 5 wins

main.py is the ONLY place that knows which arm and which camera are used. The game
engine just calls arm.ready()/pump()/show()/stop() and vision.read_gesture().
"""
import argparse

import config
from game_engine import GameEngine, Scoreboard
from game_engine.pickers import make_picker

RESULT_TEXT = {
    "player": "You win this round!",
    "arm": "The arm wins this round.",
    "draw": "It's a draw.",
}


def build_devices(mock):
    """Return (arm, vision). Imports are inside the function so that a missing
    camera or arm library only matters when that mode is actually used."""
    if mock:
        from arm_controller import MockArm
        from vision import KeyboardVision
        return MockArm(), KeyboardVision()

    from arm_controller.roarm_controller import RoArmController
    from vision.vision_module import VisionModule
    arm = RoArmController(config.ARM_HOST, config.ARM_USE_SERIAL, config.SERIAL_PORT)
    vision = VisionModule(config.CAMERA_INDEX)
    return arm, vision


def play_match(engine, board):
    """Play rounds until someone wins the match. Returns False if the engine hit an error."""
    engine.start_game()
    print(f"\nFirst to {board.rounds_to_win} wins.\n")

    rounds_played = 0
    status = engine.get_status()
    while status["state"] == "READY":
        print(f"--- Round {rounds_played + 1} ---")
        engine.play_round()
        status = engine.get_status()

        if status["state"] == "ERROR":
            print(f"Stopped because of an error: {status['error']}")
            return False

        if status["last_result"] is None:          #round cancelled, nothing was scored
            print(status["error"], "\n")
            continue

        rounds_played += 1
        print(f"You: {status['last_player_move']}   Arm: {status['last_arm_move']}")
        print(RESULT_TEXT[status["last_result"]])
        print(f"Score: You {status['player_score']} - Arm {status['arm_score']} "
              f"(draws: {status['draws']})\n")

    print("You won the match!" if board.match_winner() == "player" else "The arm won the match.")
    return True


def main():
    parser = argparse.ArgumentParser(description="Rock Paper Scissors robot arm")
    parser.add_argument("--mock", action="store_true",
                        help="use a fake arm and keyboard input instead of the real hardware")
    parser.add_argument("--mode", default=config.DEFAULT_MODE,
                        choices=["random", "frequency", "adaptive"],
                        help="how the arm picks its moves")
    parser.add_argument("--rounds", type=int, default=config.ROUNDS_TO_WIN,
                        help="rounds needed to win a match")
    args = parser.parse_args()

    try:
        arm, vision = build_devices(args.mock)
    except Exception as exc:                       # missing library, port busy, stub not written...
        print(f"Could not start the devices: {type(exc).__name__}: {exc}")
        print("Tip: run with --mock to play without the arm and camera.")
        return

    board = Scoreboard(args.rounds)
    engine = GameEngine(arm=arm, vision=vision, picker=make_picker(args.mode), scoreboard=board)

    try:
        while True:
            if not play_match(engine, board):
                break
            if input("\nPlay again? (y/n): ").strip().lower() != "y":
                break
    except KeyboardInterrupt:                      
        print("\nInterrupted.")
    finally:
        for device in (vision, arm):               # release the camera and the serial port
            close = getattr(device, "close", None)
            if close:
                close()
    print("Bye!")


if __name__ == "__main__":
    main()