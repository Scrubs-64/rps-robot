ROCK = "rock"
PAPER = "paper"
SCISSORS = "scissors"

ALL_MOVES = (ROCK, PAPER, SCISSORS)

# key beats value
BEATS = {
    ROCK: SCISSORS,
    PAPER: ROCK,
    SCISSORS: PAPER,
}

def counter_to(move):
    """Return the move that beats the current move"""    
    for winner, loser in BEATS.items():
        if loser == move:
            return winner
    raise ValueError(f"Invalid move: {move}")