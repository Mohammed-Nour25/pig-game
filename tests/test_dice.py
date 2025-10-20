import random
from pig_game.dice import Dice

def test_roll_mocked(monkeypatch):
    """Ensure Dice.roll returns mocked value in the expected range."""
    monkeypatch.setattr(random, "randint", lambda a, b: 6)
    d = Dice()
    assert d.roll() == 6
