"""AI Intelligence (skeleton).
TODO (M2):
- Implement Intelligence with levels easy/medium/hard
- Method: should_hold(turn_points, total_score, opponent_score, goal) -> bool
- ≥90% coverage, docstrings, type hints
"""

from __future__ import annotations

class Intelligence:  # pragma: no cover
    """Simple AI policy (skeleton)."""
    def __init__(self, level: str = "medium") -> None:
        raise NotImplementedError("Implement Intelligence for M2")

    def should_hold(self, turn_points: int, total_score: int, opponent_score: int, goal: int) -> bool:
        raise NotImplementedError("Implement Intelligence.should_hold for M2")
