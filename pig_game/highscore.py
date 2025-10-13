"""HighScore storage system (step 3: add rename_player).

This step sets up persistent JSON storage with minimal schema and
adds player registration and renaming support.

{
  "players": {},
  "games": []
}
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

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

    # ---------- player management ----------
    def register_player(self, name: str) -> str:
        """Register a new player or return existing player ID."""
        name = name.strip()
        if not name:
            raise ValueError("Player name cannot be empty")

        # Check if player already exists (case-insensitive)
        for pid, info in self.data["players"].items():
            if info.get("name", "").lower() == name.lower():
                return pid

        # Assign new player ID
        new_id = f"p{len(self.data['players']) + 1}"

        # Create entry
        self.data["players"][new_id] = {
            "name": name,
            "wins": 0,
            "losses": 0,
            "score": 0,
        }

        # Save automatically
        self.save()
        return new_id

    def rename_player(self, pid: str, new_name: str) -> None:
        """Rename an existing player (must not conflict with other names)."""
        new_name = new_name.strip()
        if not new_name:
            raise ValueError("New name cannot be empty")

        if pid not in self.data["players"]:
            raise KeyError(f"Player ID {pid} not found")

        # Check if another player already uses this name
        for other_pid, info in self.data["players"].items():
            if other_pid != pid and info.get("name", "").lower() == new_name.lower():
                raise ValueError(f"Name '{new_name}' already taken")

        # Update and save
        self.data["players"][pid]["name"] = new_name
        self.save()

    # ---------- results ----------
    def record_result(self, winner_pid: str, loser_pid: str) -> None:
        """Record one match result: update wins/losses and append a game log."""
        from datetime import datetime

        # Basic validation
        players = self.data.get("players", {})
        if winner_pid not in players or loser_pid not in players:
            raise KeyError("Both winner and loser must be valid player IDs")
        if winner_pid == loser_pid:
            raise ValueError("Winner and loser cannot be the same player")

        # Normalize counters (in case old rows miss some keys)
        for pid in (winner_pid, loser_pid):
            p = players[pid]
            p["wins"] = int(p.get("wins", 0))
            p["losses"] = int(p.get("losses", 0))
            # keep optional "score" if present; not required for this step

        # Update stats
        players[winner_pid]["wins"] += 1
        players[loser_pid]["losses"] += 1

        # Ensure games list exists
        games = self.data.setdefault("games", [])
        if not isinstance(games, list):
            self.data["games"] = games = []

        # Append a compact log entry (UTC ISO timestamp)
        games.append(
            {
                "winner": winner_pid,
                "loser": loser_pid,
                "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            }
        )

        # Persist
        self.save()

    # ---------- reporting ----------
    def table(self) -> list[tuple[str, str, int, int]]:
        """Return a sorted table of (pid, name, wins, losses).

        Sort order:
          - wins:  descending
          - losses: ascending
          - name:   ascending (case-insensitive)
        """
        players = self.data.get("players", {})
        rows: list[tuple[str, str, int, int]] = []

        for pid, info in players.items():
            name = str(info.get("name", ""))
            wins = int(info.get("wins", 0))
            losses = int(info.get("losses", 0))
            rows.append((pid, name, wins, losses))

        # Sort by: wins DESC, losses ASC, name ASC (case-insensitive)
        rows.sort(key=lambda r: (-r[2], r[3], r[1].lower()))
        return rows

    # ---------- helpers ----------
    def _write_json(self, content: Dict[str, Any]) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
