# pig_game/player.py
from __future__ import annotations


class Player:
    """Represents a Pig player with total and current-turn points."""

    def __init__(self, name: str = "Player") -> None:
        self.name = name
        self.total = 0
        self.turn = 0

    # --- simple scoring utility used by tests ---
    def add_points(self, points) -> None:
        """
        Add points directly to the player's TOTAL score.
        Casts input to int. Allows 0 and -0 (no-op). Negative values subtract.
        """
        self.total += int(points)

    # --- core actions for the Pig game ---
    def add_roll(self, value: int) -> int:
        """
        Apply a dice roll to this player's TURN points.
        - If value == 1 => bust: reset turn to 0.
        - Else accumulate into turn.
        Returns the roll value (tests assert on this).
        """
        value = int(value)
        if value == 1:
            self.turn = 0
        else:
            if value < 0:
                raise ValueError("roll value must be >= 0")
            self.turn += value
        return value

    def hold(self) -> str:
        """
        Bank current TURN points into TOTAL and reset TURN to 0.
        Returns 'ok' (tests assert on this exact string).
        """
        self.total += self.turn
        self.turn = 0
        return "ok"

    def reset_turn(self) -> None:
        """Lose current turn points (e.g., when rolling 1)."""
        self.turn = 0

    def reset(self) -> None:
        """Reset total and turn (used by tests)."""
        self.total = 0
        self.turn = 0

    # --- utilities ---
    def rename(self, new_name: str) -> None:
        new = (new_name or "").strip()
        if not new:
            raise ValueError("name cannot be empty")
        self.name = new

    def __repr__(self) -> str:  # helpful for tests/debugging
        return f"Player(name={self.name!r}, total={self.total}, turn={self.turn})"
