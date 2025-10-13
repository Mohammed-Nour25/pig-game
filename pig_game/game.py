"""Minimal Game core for Pig to make the CLI usable.

This baseline allows:
- `start` to create a game,
- `status` to show players/scores/turn points,
- `roll`/`hold` to follow typical Pig rules,
- later grow into AI/HighScore without breaking the interface.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

try:
    # Use team's Player if it exists.
    from pig_game.player import Player  # type: ignore
except Exception:
    @dataclass
    class Player:  # fallback minimal player
        name: str
        score: int = 0
        is_computer: bool = False


try:
    # Use team's Dice if it exists.
    from pig_game.dice import Dice  # type: ignore
except Exception:
    import random

    class Dice:  # fallback minimal dice
        def roll(self) -> int:
            return random.randint(1, 6)


class Game:
    """Core Pig game logic (minimal, two players)."""

    def __init__(self, goal_score: int = 100) -> None:
        if not isinstance(goal_score, int) or goal_score < 1:
            raise ValueError("goal_score must be a positive integer")

        self.goal_score = goal_score
        self.players: list[Player] = [Player("Player1"), Player("Player2")]
        self.active_index: int = 0
        self.turn_points: int = 0
        self._dice = Dice()

    # ---------- helpers ----------
    @property
    def active_player(self) -> int:
        """Return the index of the active player (0 or 1)."""
        return self.active_index

    def _active(self) -> Player:
        return self.players[self.active_index]

    # ---------- actions ----------
    def roll(self) -> int:
        """Roll the dice. If 1 → bust (turn_points = 0) & switch turn."""
        value = self._dice.roll()
        if value == 1:
            self.turn_points = 0
            self.switch_turn()
        else:
            self.turn_points += value
        return value

    def hold(self) -> Optional[str]:
        """Bank turn points to total score, reset, check win, then switch."""
        p = self._active()
        p.score += self.turn_points
        self.turn_points = 0

        if self.is_winner():
            # Return marker so CLI/tests can detect a win if needed.
            return "win"

        self.switch_turn()
        return None

    def switch_turn(self) -> None:
        """Switch active player (two-player rotation)."""
        self.active_index = 1 - self.active_index

    def is_winner(self) -> bool:
        """Check if the active player has reached the goal score."""
        return self._active().score >= self.goal_score

    # ---------- helpers for dev/testing ----------
    def set_names(self, p1: str, p2: str) -> None:
        """Rename both players quickly."""
        self.players[0].name = p1
        self.players[1].name = p2

    def cheat(self, points: int = 90) -> None:
        """Add points to the active player (for quick testing)."""
        if points < 0:
            points = 0
        self._active().score += points
