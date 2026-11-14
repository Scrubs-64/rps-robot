import pytest


from game_engine.scoreboard import Scoreboard


def test_starts_at_zero():
    sb = Scoreboard(3)
    assert (sb.player_score, sb.arm_score, sb.draws) == (0, 0, 0)
    assert sb.match_winner() is None


def test_record_counts_each_result():
    sb = Scoreboard(3)
    sb.record("player")
    sb.record("arm")
    sb.record("arm")
    sb.record("draw")
    assert (sb.player_score, sb.arm_score, sb.draws) == (1, 2, 1)


def test_player_wins_match():
    sb = Scoreboard(2)
    sb.record("player")
    assert sb.match_winner() is None
    sb.record("player")
    assert sb.match_winner() == "player"


def test_arm_wins_match():
    sb = Scoreboard(2)
    sb.record("arm")
    sb.record("draw")
    sb.record("arm")
    assert sb.match_winner() == "arm"


def test_reset():
    sb = Scoreboard(2)
    sb.record("player")
    sb.reset()
    assert sb.player_score == 0


def test_invalid_result_raises():
    with pytest.raises(ValueError):
        Scoreboard(3).record("banana")
