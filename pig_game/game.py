"""Game core (M1-2: Create Game class only).

Manages:
- players list (two players by default)
- per-player scores
- current turn total
- active player index
- goal score

Note:
- Gameplay actions (roll, hold, switch_turn, is_winner) are not implemented yet.
"""

from __future__ import annotations
from typing import List, Optional


class Game:
    """Core Pig game state manager (structure only)."""

    def __init__(self, goal: int = 100, players: Optional[List[str]] = None) -> None:
        """
        Initialize a new game state.

        Args:
            goal: Target score to win (must be > 0).
            players: Optional list of two player names.
                     Defaults to ["Player 1", "Player 2"].
        """
        if goal <= 0:
            raise ValueError("goal must be positive")

        self.goal: int = goal

        # Initialize players
        if players is None:
            players = ["Player 1", "Player 2"]
        if len(players) != 2:
            raise ValueError("Pig requires exactly two players")

        self.players: List[str] = players

        # Initialize scores for each player
        self.scores: List[int] = [0, 0]

        # Track current turn total and active player
        self.turn_total: int = 0
        self.active_index: int = 0  # 0 = Player 1, 1 = Player 2

    # --- Convenience properties ---
    @property
    def active(self) -> str:
        """Return the active player's name."""
        return self.players[self.active_index]

    @property
    def waiting(self) -> str:
        """Return the non-active player's name."""
        return self.players[1 - self.active_index]

    # --- Placeholders for future implementation ---
    def roll(self):
        raise NotImplementedError("Implement Game.roll in the next task")

    def hold(self):
        raise NotImplementedError("Implement Game.hold in the next task")

    def switch_turn(self):
        raise NotImplementedError("Implement Game.switch_turn in the next task")

    def is_winner(self):
        raise NotImplementedError("Implement Game.is_winner in the next task")
