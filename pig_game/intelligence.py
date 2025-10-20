# pig_game/intelligence.py
from dataclasses import dataclass


@dataclass
class Intelligence:
    """
    Simple, pluggable AI policy for the computer player.
    Levels: easy, normal, smart.
    """

    level: str = "normal"

    def should_hold(self, turn_score: int, total_score: int, opponent_score: int) -> bool:
        """
        Decide whether the computer should HOLD or ROLL.
        - HOLD if holding now would win.
        - Otherwise use a target threshold per level.
        - If trailing significantly, be slightly more aggressive.
        """
        WIN_SCORE = 100
        if total_score + turn_score >= WIN_SCORE:
            return True

        targets = {"easy": 15, "normal": 20, "smart": 25}
        target = targets.get(self.level, 20)

        # If trailing by a noticeable margin, raise risk tolerance.
        if total_score + 15 < opponent_score:
            target += 3

        return turn_score >= target
