# pig_game/intelligence.py
from __future__ import annotations

from typing import Final


class Intelligence:
    """
    Tiny policy for CPU decisions in Pig.

    Levels:
        - easy   : hold when turn_points >= 15
        - normal : hold when turn_points >= 20 (alias: medium)
        - hard   : hold when total_score + turn_points >= goal - 10 (alias: smart)
    """

    EASY_THRESHOLD: Final[int] = 15
    NORMAL_THRESHOLD: Final[int] = 20

    def __init__(self, level: str = "normal") -> None:
        # Normalize aliases coming from different parts of the code/CLI
        lvl = level.lower()
        if lvl == "medium":
            lvl = "normal"
        if lvl == "smart":
            lvl = "hard"
        if lvl not in ("easy", "normal", "hard"):
            raise ValueError(
                "Invalid level "
                f"'{level}'. Choose from 'easy', 'normal' (or 'medium'), 'hard' (or 'smart')."
            )
        self.level = lvl

    def should_hold(
        self,
        turn_points: int,
        total_score: int,
        opponent_score: int,  # currently unused; kept for future strategies
        goal: int = 100,
    ) -> bool:
        """Return True if the CPU should hold this turn."""
        if self.level == "easy":
            return turn_points >= self.EASY_THRESHOLD
        if self.level == "normal":
            return turn_points >= self.NORMAL_THRESHOLD
        # hard
        return (total_score + turn_points) >= (goal - 10)
