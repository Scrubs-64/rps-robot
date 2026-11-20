from arm_controller import MockArm
from game_engine import GameEngine, Scoreboard

class SpyPicker:
    def __init__(self, calls): self.calls = calls
    def choose_move(self, history):
        self.calls.append("commit")
        return "rock"

class SpyVision:
    def __init__(self, calls): self.calls = calls
    def read_gesture(self):
        self.calls.append("capture")
        return "paper"

def test_arm_commits_before_capture():
    calls = []
    engine = GameEngine(MockArm(), SpyVision(calls), SpyPicker(calls), Scoreboard(3))
    engine.start_game()
    engine.play_round()
    assert calls == ["commit", "capture"]