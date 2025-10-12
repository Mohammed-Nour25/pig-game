# tests/test_game.py
import pytest

from pig_game.game import Game


# Helper: monkeypatch random.randint with a deterministic sequence
def use_dice_sequence(monkeypatch, sequence):
    it = iter(sequence)

    def fake_randint(a, b):
        try:
            return next(it)
        except StopIteration:
            return 1  # default to bust if sequence is exhausted

    monkeypatch.setattr("pig_game.game.random.randint", fake_randint)


def test_initial_state_defaults():
    g = Game(goal=50)
    assert g.goal == 50
    assert g.players == ["Player 1", "Player 2"]
    assert g.scores == [0, 0]
    assert g.turn_total == 0
    assert g.active_index == 0
    assert g.active == "Player 1"
    assert g.waiting == "Player 2"


def test_roll_adds_to_turn_total_non_one(monkeypatch):
    use_dice_sequence(monkeypatch, [3, 4])
    g = Game()
    v1 = g.roll()
    v2 = g.roll()
    assert v1 == 3 and v2 == 4
    assert g.turn_total == 7
    assert g.active_index == 0


def test_roll_bust_on_one_switches(monkeypatch):
    use_dice_sequence(monkeypatch, [1])
    g = Game()
    v = g.roll()
    assert v == 1
    assert g.turn_total == 0
    assert g.active_index == 1


def test_hold_banks_points_and_switches(monkeypatch):
    use_dice_sequence(monkeypatch, [5])
    g = Game()
    g.roll()
    g.hold()
    assert g.scores == [5, 0]
    assert g.turn_total == 0
    assert g.active_index == 1


def test_hold_on_winning_does_not_switch(monkeypatch):
    use_dice_sequence(monkeypatch, [6])
    g = Game(goal=6)
    g.roll()
    g.hold()
    assert g.scores[0] == 6
    assert g.active_index == 0
    assert g.is_winner(0)


def test_switch_turn_manual_toggle():
    g = Game()
    g.switch_turn()
    assert g.active_index == 1
    g.switch_turn()
    assert g.active_index == 0


def test_is_winner_with_explicit_index(monkeypatch):
    use_dice_sequence(monkeypatch, [4, 4, 4])
    g = Game(goal=8)
    g.roll()
    g.roll()  # turn_total = 8
    g.hold()  # player 1 banks 8 and wins
    assert g.is_winner(0) is True
    assert g.is_winner(1) is False


def test_multiple_turns_accumulate_scores(monkeypatch):
    # P1: roll 3, hold -> +3; P2: bust 1; P1: 4, hold -> +4 (total 7)
    use_dice_sequence(monkeypatch, [3, 1, 4])
    g = Game(goal=20)
    g.roll()
    g.hold()
    assert g.scores == [3, 0] and g.active_index == 1
    g.roll()  # bust -> switch
    assert g.active_index == 0 and g.turn_total == 0
    g.roll()
    g.hold()
    assert g.scores == [7, 0]


def test_cheat_adds_90_points():
    g = Game()
    before = g.scores[0]
    g.cheat()
    assert g.scores[0] == before + 90
    assert g.scores[1] == 0


def test_goal_must_be_positive():
    with pytest.raises(ValueError):
        Game(goal=0)
    with pytest.raises(ValueError):
        Game(goal=-10)


def test_requires_exactly_two_players():
    with pytest.raises(ValueError):
        Game(players=["Only One"])
    with pytest.raises(ValueError):
        Game(players=["A", "B", "C"])


def test_roll_then_hold_boundary(monkeypatch):
    # Ensure state resets correctly after hold and next player's roll works
    use_dice_sequence(monkeypatch, [5, 6, 2])
    g = Game(goal=20)
    g.roll()
    g.hold()  # P1 banks 5
    assert g.scores == [5, 0] and g.turn_total == 0 and g.active_index == 1
    v = g.roll()
    assert v == 6 and g.turn_total == 6 and g.active_index == 1
    g.hold()  # P2 banks 6
    assert g.scores == [5, 6]
    v2 = g.roll()  # Back to P1
    assert v2 == 2 and g.turn_total == 2 and g.active_index == 0
