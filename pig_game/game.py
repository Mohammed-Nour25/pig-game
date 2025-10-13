"""Minimal Game core for Pig to make the CLI usable (robust to partial M1)."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

# ---------- Fallback types ----------
@dataclass
class _FallbackPlayer:
    name: str
    score: int = 0
    is_computer: bool = False


class _FallbackDice:
    import random

    def roll(self) -> int:
        return self.random.randint(1, 6)


# ---------- Safe factories ----------
def _make_player(name: str):
    """Try to build the team's Player; fall back to a tiny local one."""
    try:
        from pig_game.player import Player  # type: ignore
        try:
            return Player(name)  # type: ignore[call-arg]
        except Exception:
            # Class موجودة لكن غير جاهزة — نرجع fallback
            return _FallbackPlayer(name)
    except Exception:
        # Module/player غير موجود — نرجع fallback
        return _FallbackPlayer(name)


def _make_dice():
    """Try to build the team's Dice; fall back to a tiny local one."""
    try:
        from pig_game.dice import Dice  # type: ignore
        try:
            return Dice()  # type: ignore[call-arg]
        except Exception:
            return _FallbackDice()
    except Exception:
        return _FallbackDice()


class Game:
    """Core Pig game logic (minimal, two players)."""

    def __init__(self, goal_score: int = 100) -> None:
        if not isinstance(goal_score, int) or goal_score < 1:
            raise ValueError("goal_score must be a positive integer")

        self.goal_score = goal_score
        self.players = [_make_player("Player1"), _make_player("Player2")]
        self.active_index: int = 0
        self.turn_points: int = 0
        self._dice = _make_dice()

    # ---------- helpers ----------
    @property
    def active_player(self) -> int:
        return self.active_index

    def _active(self):
        return self.players[self.active_index]

    # ---------- actions ----------
    def roll(self) -> int:
        """Roll the dice. If 1 → bust (turn_points = 0) & switch turn."""
        value = int(self._dice.roll())
        if value == 1:
            self.turn_points = 0
            self.switch_turn()
        else:
            self.turn_points += value
        return value

    def hold(self) -> Optional[str]:
        """Bank turn points to total score, reset, check win, then switch."""
        p = self._active()
        # player may expose `score` or `total_score`
        if hasattr(p, "score"):
            p.score += self.turn_points  # type: ignore[attr-defined]
        elif hasattr(p, "total_score"):
            p.total_score += self.turn_points  # type: ignore[attr-defined]
        self.turn_points = 0

        if self.is_winner():
            return "win"

        self.switch_turn()
        return None

    def switch_turn(self) -> None:
        self.active_index = 1 - self.active_index

    def is_winner(self) -> bool:
        p = self._active()
        total = getattr(p, "score", getattr(p, "total_score", 0))
        return int(total) >= int(self.goal_score)

    # ---------- helpers for dev/testing ----------
    def set_names(self, p1: str, p2: str) -> None:
        self.players[0].name = p1
        self.players[1].name = p2

    def cheat(self, points: int = 90) -> None:
        if points < 0:
            points = 0
        p = self._active()
        if hasattr(p, "score"):
            p.score += points  # type: ignore[attr-defined]
        elif hasattr(p, "total_score"):
            p.total_score += points  # type: ignore[attr-defined]
