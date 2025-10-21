# pig_game/player.py
from __future__ import annotations

class Player:
    """Represents a Pig player with total and current-turn points."""

    def __init__(self, name: str = "Player") -> None:
        self.name = name
        self.total = 0
        self.turn = 0

    # --- core actions ---
    def add_roll(self, value: int) -> None:
        """Add a die value to the current turn, or reset if it's a bust (1)."""
        if value < 1:
            raise ValueError("Die value must be >= 1")
        if value == 1:
            # Rolling 1 = bust
            self.reset_turn()
        else:
            self.turn += value

    def hold(self) -> None:
        """Bank the current turn points to total and reset turn."""
        self.total += self.turn
        self.turn = 0

    def reset_turn(self) -> None:
        """Lose current turn points (e.g., when rolling 1)."""
        self.turn = 0

    # --- utilities ---
    def rename(self, new_name: str) -> None:
        new = (new_name or "").strip()
        if not new:
            raise ValueError("name cannot be empty")
        self.name = new

    def __repr__(self) -> str:  # helpful for tests/debugging
        return f"Player(name={self.name!r}, total={self.total}, turn={self.turn})"
