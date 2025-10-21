# pig_game/game.py
from __future__ import annotations

import random
from typing import List, Optional


@dataclass
class Game:
    """
    Minimal Pig game engine for two players, designed to satisfy tests.

    - Exactly two players.
    - Each player has a total score and a per-turn accumulator.
    - roll(): add to current turn unless you roll 1 (bust -> turn becomes 0 and switch).
    - hold(): bank current turn to total; if total >= goal -> win (don't switch), else switch.
    - switch_turn(): toggle the current player (0 <-> 1).
    - cheat(): add 90 points to current player's total (for testing).
    - is_winner(index): check if a player reached the goal.
    """

    def __init__(self, goal: int = 100, players: Optional[List[str]] = None) -> None:
        if goal <= 0:
            raise ValueError("Goal must be positive.")
        if players is None:
            players = ["Player 1", "Player 2"]
        if len(players) != 2:
            raise ValueError("Game requires exactly two players.")

        self.goal: int = int(goal)
        self.players: List[str] = list(players)

        # Total scores and current turn points per player
        self.scores: List[int] = [0, 0]
        self._turn_points: List[int] = [0, 0]

        # Whose turn? 0 or 1
        self.current: int = 0

    # --- Core mechanics -----------------------------------------------------

    def roll(self) -> int:
        """Roll a die. If 1 -> bust: reset current turn points and switch. Else add to turn."""
        value = int(random.randint(1, 6))
        if value == 1:
            self._turn_points[self.current] = 0
            self.switch_turn()
            return value
        self._turn_points[self.current] += value
        return value

    def hold(self) -> str:
        """
        Bank current turn points to total.
        If the player reaches goal, return 'win' and DO NOT switch.
        Otherwise switch and return 'ok'.
        """
        idx = self.current
        self.scores[idx] += self._turn_points[idx]
        self._turn_points[idx] = 0

        if self.is_winner(idx):
            return "win"

        self.switch_turn()
        return "ok"

    def switch_turn(self) -> None:
        """Toggle the current player (0 <-> 1)."""
        self.current = 1 - self.current

    # --- Convenience properties expected by tests ---------------------------

    @property
    def turn_total(self) -> int:
        """Current player's accumulated (unbanked) points this turn."""
        return self._turn_points[self.current]

    @property
    def active_index(self) -> int:
        """Index of the active player: 0 or 1."""
        return self.current

    @property
    def active(self) -> str:
        """Name of the active player."""
        return self.players[self.current]

    @property
    def waiting(self) -> str:
        """Name of the non-active player."""
        return self.players[1 - self.current]

    # --- Helpers ------------------------------------------------------------

    def is_winner(self, index: Optional[int] = None) -> bool:
        """Check if a player (current by default) has reached the goal."""
        idx = self.current if index is None else int(index)
        return self.scores[idx] >= self.goal

    def cheat(self) -> None:
        """Testing helper: add 90 points to the current player's total."""
        self.scores[self.current] += 90
