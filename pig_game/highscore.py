import json
from pathlib import Path
from typing import Dict, Any, List

DEFAULT_PATH = Path.home() / ".pig_highscores.json"


class HighScore:
    """JSON-backed highscore store with basic player stats and game logs."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = Path(path) if path else DEFAULT_PATH
        self.data: Dict[str, Any] = {"players": {}, "games": []}
        self._load()

    # ---------- persistence ----------
    def _load(self) -> None:
        """Load JSON from disk; if it fails, start fresh."""
        if self.path.exists():
            try:
                self.data = json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                self.data = {"players": {}, "games": []}

    def _save(self) -> None:
        """Persist JSON to disk."""
        self.path.write_text(
            json.dumps(self.data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    # ---------- players ----------
    def register_player(self, name: str) -> str:
        """Ensure a player entry exists and return its id (here, the name)."""
        key = (name or "").strip()
        if not key:
            raise ValueError("empty name")
        players = self.data["players"]
        if key not in players:
            players[key] = {"wins": 0, "losses": 0}
            self._save()
        return key

    def rename_player(self, old: str, new: str) -> None:
        """Rename a player, preserving stats; prevent collisions."""
        old = (old or "").strip()
        new = (new or "").strip()
        if not new:
            raise ValueError("empty new name")
        players = self.data["players"]
        if old not in players:
            raise KeyError(old)
        if new in players and new != old:
            raise ValueError("name already exists")
        players[new] = players.pop(old)
        self._save()

    # ---------- results ----------
    def record_result(self, winner: str, loser: str, for_points: int, against_points: int) -> None:
        """Record a single finished game result and update stats."""
        self.register_player(winner)
        self.register_player(loser)
        self.data["players"][winner]["wins"] += 1
        self.data["players"][loser]["losses"] += 1
        self.data["games"].append(
            {"winner": winner, "loser": loser, "for": for_points, "against": against_points}
        )
        self._save()

    def top(self, limit: int = 10) -> List[dict]:
        """Return top players by wins desc, losses asc, name asc."""
        items = [
            {"player": name, "wins": p["wins"], "losses": p["losses"]}
            for name, p in self.data["players"].items()
        ]
        items.sort(key=lambda x: (-x["wins"], x["losses"], x["player"].lower()))
        return items[: max(1, limit)]

    # ---------- helpers expected by some tests ----------
    def table(self):
        """Return a list of (player_id, name, wins, losses) tuples for display."""
        rows = []
        for name, stats in self.data["players"].items():
            rows.append((name, name, stats["wins"], stats["losses"]))
        rows.sort(key=lambda x: (-x[2], x[3], x[0].lower()))
        return rows

    def add_result(self, p1: str, p2: str, *, winner: str, score_for: int, score_against: int, duration_sec: int = 0):
        """Alias to record_result() for compatibility with some tests."""
        loser = p2 if winner == p1 else p1
        self.record_result(winner, loser, score_for, score_against)

    def add_game(self, p1: str, p2: str, *, winner: str, score_for: int, score_against: int, duration_sec: int = 0):
        """Another alias forwarding to add_result()."""
        self.add_result(p1, p2, winner=winner, score_for=score_for, score_against=score_against, duration_sec=duration_sec)

