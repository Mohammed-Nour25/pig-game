import pytest
from pig_game.player import Player

def test_player_roll_and_hold():
    """Accumulate turn points then hold to bank them into total."""
    p = Player("A")
    p.add_roll(3)
    p.add_roll(4)
    assert p.turn == 7
    p.hold()
    assert p.total == 7
    assert p.turn == 0

def test_player_bust_resets_turn():
    """Rolling 1 resets the turn points to zero."""
    p = Player()
    p.add_roll(5)
    p.add_roll(1)
    assert p.turn == 0

def test_rename_validation():
    """Renaming requires a non-empty, non-blank string."""
    p = Player()
    with pytest.raises(ValueError):
        p.rename("")
    p.rename("Ali")
    assert p.name == "Ali"
