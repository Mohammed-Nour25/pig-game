"""Player model with minimal functionality to support tests."""

from __future__ import annotations


class Player:
    """Represents a Pig game player with name, total score, and turn points."""

    def __init__(self, name: str, score: int = 0, is_computer: bool = False) -> None:
        # Basic fields with safe casting
        self.name: str = str(name)
        self.total: int = int(score)
        self.turn: int = 0
        self.is_computer: bool = bool(is_computer)

    # --- Gameplay helpers ---
    def add_roll(self, value: int) -> int:
        """Add a dice roll to the current turn; if 1, bust (turn -> 0)."""
        v = int(value)
        if v == 1:
            self.turn = 0
        else:
            self.turn += v
        return v

    def hold(self) -> str:
        """Bank current turn points to total, then reset turn."""
        self.total += self.turn
        self.turn = 0
        return "ok"

    def reset(self) -> None:
        """Reset scores (used by older placeholder tests)."""
        self.total = 0
        self.turn = 0

    # --- API used by the new Player tests ---
    def add_points(self, points: int) -> None:
        """Directly add points to total (used by unit tests)."""
        self.total += int(points)

    def rename(self, new_name: str) -> None:
        """Rename the player (no validation needed for tests)."""
        self.name = str(new_name)

    # --- Introspection ---
    def __repr__(self) -> str:
        # Must contain the word "Player" for tests
        return (
            f"Player(name={self.name!r}, total={self.total}, "
            f"turn={self.turn}, is_computer={self.is_computer})"
        )
