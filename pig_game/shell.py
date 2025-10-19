# pig_game/shell.py
from __future__ import annotations

import argparse
import sys
import time
from typing import Any, List, Optional, Tuple

from pig_game.game import Game
from pig_game.intelligence import Intelligence

# HighScore integration is optional. We try to import it; if not available,
# the CLI still works and simply skips recording or showing highscores.
try:
    from pig_game.highscore import HighScoreStore, make_entry  # type: ignore
except Exception:  # pragma: no cover - safety net
    HighScoreStore = None  # type: ignore[misc,assignment]
    make_entry = None  # type: ignore[misc,assignment]


# ---------- helpers for game state ----------


def _game_over(g: Game) -> bool:
    """Return True if either player has won (by API or by reaching goal)."""
    # Preferred: use provided winner-API if exists.
    try:
        if g.is_winner(0) or g.is_winner(1):
            return True
    except Exception:
        pass

    # Fallback: rely on totals vs goal.
    try:
        return any(s >= g.goal for s in g.scores)  # type: ignore[attr-defined]
    except Exception:
        return False


def _winner_index(g: Game) -> Optional[int]:
    """Return 0 if Player 1 wins, 1 if Player 2 wins, else None."""
    try:
        if g.is_winner(0):
            return 0
        if g.is_winner(1):
            return 1
    except Exception:
        pass

    # Fallback by total scores if API not present.
    try:
        if g.scores[0] >= g.goal or g.scores[1] >= g.goal:  # type: ignore[attr-defined]
            return 0 if g.scores[0] >= g.scores[1] else 1  # type: ignore[attr-defined]
    except Exception:
        pass
    return None


# ---------- optional HighScore wrapper ----------


class _NoHighScoreStore:
    """Tiny no-op store used when HighScore module is not available."""

    def add(self, *_: Any, **__: Any) -> None:  # pylint: disable=unused-argument
        print("Note: HighScore module not available, result was not recorded.")

    def top(self, _n: int = 10) -> list:
        print("Note: HighScore
