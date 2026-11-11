from enum import Enum, auto


class GameState(Enum):
    
    IDLE = auto()       #Nothing is running
    READY = auto()      #Game started, arm is ready
    COMMIT = auto()     #Move is chosen
    COUNTDOWN = auto()  #The 3 pumps before showing move
    CAPTURE = auto()    #Reading the player's hand
    RETRY = auto()      #No gesture detected
    REVEAL = auto()     #Arm shows its move
    RESULT = auto()     #Winner decided
    GAME_OVER = auto()  #Winning score reached(by arm or player)
    ERROR = auto()      #Something failed :(