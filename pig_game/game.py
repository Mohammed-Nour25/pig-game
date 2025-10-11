"""Game core (skeleton).
TODO (M1):
- Manage players, scores, turn_total, active player, goal
- roll(): add dice to turn_total; if 1 => bust (turn_total=0) and switch turn
- hold(): bank turn_total, reset, switch, check winner
- switch_turn(), is_winner()
- Support two human players
- Placeholder for cheat (+90)
- Unit tests ≥10 tests, ≥20 assertions, docstrings, ≥90% coverage
"""

from __future__ import annotations

class Game:  # pragma: no cover
    """Core Pig game logic (skeleton)."""
    def __init__(self, goal: int = 100) -> None:
        raise NotImplementedError("Implement Game for M1")

    def roll(self):
        raise NotImplementedError("Implement Game.roll for M1")

    def hold(self):
        raise NotImplementedError("Implement Game.hold for M1")

    def switch_turn(self):
        raise NotImplementedError("Implement Game.switch_turn for M1")

    def is_winner(self):
        raise NotImplementedError("Implement Game.is_winner for M1")
