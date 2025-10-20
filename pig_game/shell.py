# pig_game/shell.py
from __future__ import annotations

from typing import Any, Optional
from pig_game.game import Game

# --- Optional HighScore integration (safe even if module is missing) ---
try:
    # pylint: disable=import-error,no-name-in-module
    from pig_game.highscore import HighScoreStore as _HS, make_entry as _ME  # type: ignore

    HighScoreStore = _HS  # re-export for local use/type hints
    make_entry = _ME
except Exception:  # pragma: no cover - safety net if module not present

    class HighScoreStore:  # type: ignore
        """No-op store used when the real HighScore module is not available."""

        def add(self, *args: Any, **kwargs: Any) -> None:  # pylint: disable=unused-argument
            print("Note: highscores are disabled (module not available).")

        def top(self, _n: int = 10) -> list:
            print("Note: highscores are disabled (module not available).")
            return []

    def make_entry(**kwargs: Any) -> dict:  # type: ignore
        """Fallback entry factory returning a plain dict."""
        return kwargs


# ---------- Helpers for game state ----------


def _game_over(g: Game) -> bool:
    """Return True if either player has won (by API or by reaching goal)."""
    # Preferred: dedicated API if available.
    try:
        if g.is_winner(0) or g.is_winner(1):  # type: ignore[attr-defined]
            return True
    except Exception:
        pass

    # Fallback: totals vs goal.
    try:
        return any(s >= g.goal for s in g.scores)  # type: ignore[attr-defined]
    except Exception:
        return False


def _winner_index(g: Game) -> Optional[int]:
    """Return 0 if Player 1 wins, 1 if Player 2 wins, else None."""
    try:
        if g.is_winner(0):  # type: ignore[attr-defined]
            return 0
        if g.is_winner(1):  # type: ignore[attr-defined]
            return 1
    except Exception:
        pass

    # Fallback by totals if API not present.
    try:
        if g.scores[0] >= g.goal or g.scores[1] >= g.goal:  # type: ignore[attr-defined]
            return 0 if g.scores[0] >= g.scores[1] else 1  # type: ignore[attr-defined]
    except Exception:
        pass
    return None


# ---------- Minimal entry point (keeps pylint happy, works with __main__) ----------


def main() -> int:
    """Thin entry point. The interactive CLI is provided elsewhere in the project."""
    # Keep it simple so importing/exec via `python -m pig_game` never crashes.
    print("Pig CLI entrypoint is available. Launch the full CLI from the project’s main mode.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
