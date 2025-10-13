"""HighScore storage system (step 1: load/save JSON only).

This step sets up persistent JSON storage with a minimal schema:
{
  "players": {},
  "games": []
}
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any


DATA_DIR = Path("pig_game") / "data"
DEFAULT_PATH = DATA_DIR / "highscores.json"


class HighScore:
    """Basic JSON storage for player and game data."""

    def __init__(self, path: str | Path = DEFAULT_PATH) -> None:
        self.path: Path = Path(path)
        # In-memory structure; will be overwritten by `load()`.
        self.data: Dict[str, Any] = {"players": {}, "games": []}
        self.load()

    # ---------- persistence ----------
    def load(self) -> None:
        """Load JSON file; if missing or invalid, create a fresh one."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write_json({"players": {}, "games": []})
            self.data = {"players": {}, "games": []}
            return

        try:
            with self.path.open("r", encoding="utf-8") as f:
                self.data = json.load(f)
        except (json.JSONDecodeError, OSError):
            # If file is empty/corrupted, reset to a minimal valid schema.
            self.data = {"players": {}, "games": []}
            self._write_json(self.data)

        # Normalize minimal keys if they are missing
        if "players" not in self.data or not isinstance(self.data["players"], dict):
            self.data["players"] = {}
        if "games" not in self.data or not isinstance(self.data["games"], list):
            self.data["games"] = []

    def save(self) -> None:
        """Save current data to JSON file."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._write_json(self.data)

    # ---------- helpers ----------
    def _write_json(self, content: Dict[str, Any]) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
