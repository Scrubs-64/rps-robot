from game_engine.engine import GameEngine
from gesture_recognition import GestureRecognition
from game_engine import scoreboard

vision = GestureRecognition()
engine = GameEngine()
vision.start()

