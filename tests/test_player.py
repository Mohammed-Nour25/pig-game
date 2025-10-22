import pytest
from pig_game.player import Player


# Keep only this placeholder test skipped (not the whole file)
@pytest.mark.skip(reason="Skeleton-only placeholder, not part of this assignment.")
def test_player_reset():
    pass


def test_player_bust_resets_turn():
    """Rolling 1 resets the turn points to zero."""
    p = Player()
    p.add_roll(5)
    p.add_roll(1)
    assert p.turn == 0


# --- Extra tests to raise coverage for Player ---


def test_add_zero_points_is_allowed():
    p = Player("Alice")
    p.add_points(0)
    assert p.total == 0


def test_multiple_renames():
    p = Player("Alice")
    p.rename("Bobby")
    p.rename("Charlie")
    assert p.name == "Charlie"


def test_repr_contains_player_word():
    p = Player("Dana")
    assert "Player" in repr(p)


def test_name_with_numbers():
    p = Player("Alice")
    p.rename("Ali123")
    assert p.name == "Ali123"


def test_add_large_points():
    p = Player("Big")
    p.add_points(1_000_000)
    assert p.total == 1_000_000


def test_score_accumulation_multiple_adds():
    p = Player("Sum")
    p.add_points(3)
    p.add_points(7)
    assert p.total == 10


# --- Extra coverage tests for Player core methods ---


def test_add_roll_accumulates_and_busts():
    p = Player("Rolla")
    v1 = p.add_roll(4)
    v2 = p.add_roll(3)
    assert (v1, v2) == (4, 3)
    assert p.turn == 7 and p.total == 0  # still in turn

    v3 = p.add_roll(1)  # bust
    assert v3 == 1
    assert p.turn == 0 and p.total == 0  # bust resets turn only


def test_hold_banks_and_resets_turn():
    p = Player("Holder")
    p.add_roll(5)
    p.add_roll(2)
    status = p.hold()
    assert status == "ok"
    assert p.total == 7 and p.turn == 0

    # Another small turn then hold again
    p.add_roll(3)
    p.hold()
    assert p.total == 10 and p.turn == 0


def test_reset_clears_scores_and_turn():
    p = Player("Resetter")
    p.add_points(12)
    p.add_roll(4)
    assert p.total == 12 and p.turn == 4
    p.reset()
    assert p.total == 0 and p.turn == 0


def test_add_points_casts_to_int_and_allows_negative_zero():
    p = Player("Caster")
    p.add_points(0)
    p.add_points(+5)
    p.add_points(-2)
    # total should be 3
    assert p.total == 3


def test_rename_is_applied_and_reflected_in_repr():
    p = Player("X")
    p.rename("Y")
    r = repr(p)
    assert p.name == "Y" and "Player" in r and "Y" in r
