from dataclasses import dataclass, field
from typing import Optional
from .dice import Dice
from .player import Player

@dataclass
class Game:
    """Game state for the Pig dice game."""
    goal: int = 100
    dice: Dice = field(default_factory=Dice)
    p1: Player = field(default_factory=lambda: Player("Player1"))
    p2: Player = field(default_factory=lambda: Player("Player2"))
    active: int = 1  # 1 or 2

    def current(self) -> Player:
        """Return the currently active player."""
        return self.p1 if self.active == 1 else self.p2

    def opponent(self) -> Player:
        """Return the opponent of the active player."""
        return self.p2 if self.active == 1 else self.p1

    def start(self, goal: int | None = None) -> None:
        """Start or restart the game with an optional goal."""
        if goal is not None:
            if goal < 1:
                raise ValueError("goal must be positive")
            self.goal = goal
        # Reset players and active turn
        self.p1.total = self.p1.turn = 0
        self.p2.total = self.p2.turn = 0
        self.active = 1

    def roll(self) -> int:
        """Roll the die; apply bust/switch or accumulate turn points."""
        v = self.dice.roll()
        if v == 1:
            self.current().reset_turn()
            self._switch()
        else:
            self.current().add_roll(v)
        return v

    def hold(self) -> None:
        """Hold: bank current turn points and possibly switch to opponent."""
        self.current().hold()
        if not self.is_winner(self.current()):
            self._switch()

    def is_winner(self, player: Optional[Player] = None) -> bool:
        """Check if a player has reached or exceeded the goal."""
        player = player or self.current()
        return player.total >= self.goal

    def _switch(self) -> None:
        """Switch the active player."""
        self.active = 2 if self.active == 1 else 1


