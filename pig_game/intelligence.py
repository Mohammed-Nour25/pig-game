# pig_game/intelligence.py
from typing import Final

class Intelligence:
    """
    Simple AI policy for the computer player.
    
    Levels:
        - easy: hold when turn_points >= 15
        - medium: hold when turn_points >= 20
        - hard: hold when total + turn >= goal - 10
    """

    EASY_THRESHOLD: Final[int] = 15
    MEDIUM_THRESHOLD: Final[int] = 20

    def __init__(self, level: str = "medium") -> None:
        if level not in ("easy", "medium", "hard"):
            raise ValueError(f"Invalid level '{level}'. Choose from 
'easy', 'medium', 'hard'.")
        self.level = level

    def should_hold(self, turn_points: int, total_score: int, 
opponent_score: int, goal: int) -> bool:
        """
        Decide whether the computer should HOLD or ROLL.

        Parameters
        ----------
        turn_points : int
            Current turn points accumulated.
        total_score : int
            AI's total score before this turn.
        opponent_score : int
            The opponent's current score (not used by current heuristics).
        goal : int
            The target score to win the game.
        
        Returns
        -------
        bool
            True if AI decides to hold, False otherwise.
        """
        if self.level == "easy":
            return turn_points >= self.EASY_THRESHOLD
        if self.level == "medium":
            return turn_points >= self.MEDIUM_THRESHOLD
        # hard
        return (total_score + turn_points) >= (goal - 10)

