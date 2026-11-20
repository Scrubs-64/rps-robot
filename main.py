from game_engine.engine import GameEngine
from gesture_recognition import GestureRecognition
from game_engine import scoreboard
from UI.scoreboard_ui import ScoreboardUI

vision = GestureRecognition()
engine = GameEngine()
vision.start()

