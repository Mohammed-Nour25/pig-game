"""Player module (skeleton).
TODO (M1):
- Implement Player dataclass: name, score=0, is_computer=False
- Add reset() method
"""

from __future__ import annotations

class Player:  # pragma: no cover
    """Represents a player (skeleton)."""
    def __init__(self, name: str, score: int = 0, is_computer: bool = False) -> None:
        raise NotImplementedError("Implement Player for M1")

    def reset(self) -> None:
        raise NotImplementedError("Implement Player.reset for M1")
