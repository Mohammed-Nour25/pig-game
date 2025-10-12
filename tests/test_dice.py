import pytest
import random
from pig_game.dice import Dice


def test_roll_returns_between_1_and_6(monkeypatch):
    """Check that Dice.roll() returns a mocked value correctly."""
    monkeypatch.setattr(random, "randint", lambda a, b: 4)
    dice = Dice()
    result = dice.roll()
    assert result == 4


def test_roll_in_valid_range(monkeypatch):
    """Check that Dice.roll() returns values in the valid range."""
    values = [1, 3, 6]
    monkeypatch.setattr(random, "randint", lambda a, b: values.pop(0))
    dice = Dice()
    assert dice.roll() == 1
    assert dice.roll() == 3
    assert dice.roll() == 6


def test_sides_constant():
    """Ensure Dice.SIDES is correctly set to 6."""
    dice = Dice()
    assert dice.SIDES == 6


def test_multiple_rolls_within_range():
    """Check that multiple rolls always return values between 1 and 
SIDES."""
    dice = Dice()
    for _ in range(100):
        result = dice.roll()
        assert 1 <= result <= dice.SIDES

