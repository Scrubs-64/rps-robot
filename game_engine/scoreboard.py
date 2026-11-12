class Scoreboard:
    """Keeps score for one match (first to `rounds_to_win` wins)."""

    def __init__(self, rounds_to_win=3):
        self.rounds_to_win = rounds_to_win
        self.player_score = 0
        self.arm_score = 0
        self.draws = 0

    def record(self, result):
        if result == "player":
            self.player_score += 1
        elif result == "arm":
            self.arm_score += 1
        elif result == "draw":
            self.draws += 1
        else:
            raise ValueError(f"Invalid result: {result}")

    def match_winner(self):
        if self.player_score >= self.rounds_to_win:
            return "player"
        if self.arm_score >= self.rounds_to_win:
            return "arm"
        return None

    def reset(self):
        self.player_score = 0
        self.arm_score = 0
        self.draws = 0