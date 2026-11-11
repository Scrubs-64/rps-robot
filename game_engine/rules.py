from common.moves import ALL_MOVES, BEATS


def decide_winner(player_move, arm_move):
    """Return 'player', 'arm' or 'draw'. Raise ValueError on invalid moves."""

    if player_move not in ALL_MOVES:
        raise ValueError(f"Invalid player move: {player_move}")
    if arm_move not in ALL_MOVES:
        raise ValueError(f"Invalid arm move: {arm_move}")
    if player_move==arm_move:
        return "draw"
    elif BEATS[player_move]==arm_move:
        return "player"
    else:
        return "arm"
    