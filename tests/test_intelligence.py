# tests/test_intelligence.py
import pytest
from pig_game.intelligence import Intelligence


@pytest.mark.parametrize(
    "level,turn_points,total,opponent,goal,expected",
    [
        ("easy", 15, 0, 0, 100, True),
        ("easy", 14, 0, 0, 100, False),
        ("medium", 20, 0, 0, 100, True),   # 'medium' accepted as a synonym for 'normal'
        ("medium", 19, 0, 0, 100, False),
        ("hard", 5, 80, 0, 100, False),
        ("hard", 15, 85, 0, 100, True),
    ],
)
def test_should_hold_behavior(level, turn_points, total, opponent, goal, expected):
    ai = Intelligence(level)
    assert ai.should_hold(turn_points, total, opponent, goal) is expected


def test_invalid_level_raises_error():
    with pytest.raises(ValueError):
        Intelligence("unknown")

