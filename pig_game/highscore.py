from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

# In-file JSON schema:
# {
#   "players": { "<pid>": {"name": "<Display>", "wins": 0, "losses": 0}, ... },
#   "games": [
#       {
#           "p1": "<pid1>", "p2": "<pid2>",
#           "winner": "<pid>", "loser": "<pid>",
#           "score_for": 0, "score_against": 0,
#           "duration_sec": 0,
#           "when_utc": "YYYY-MM-DDTHH:MM:SSZ",
#           "timestamp": "same-as-when_utc"
#       }, ...
#   ]
# }

DEFAULT_SCHEMA: Dict[str, Any] = {"players": {}, "games": []}


@dataclass
class GameRecord:
    """Single persisted game row."""
    p1: str
    p2: str
    winner: str
    score_for: int
    score_against: int
    duration_sec: int
    when_utc: str  # ISO-8601 UTC string (with trailing Z)


def _canonical(name: str) -> str:
    """Normalize a player identifier (case-insensitive)."""
    return name.strip().lower()


def _empty_schema() -> Dict[str, Any]:
    """Return a fresh empty schema (no shared nested dict/list)."""
    return {"players": {}, "games": []}


def _normalize_schema(data: Dict[str, Any] | None) -> Dict[str, Any]:
    """Make sure loaded JSON has the expected shape/keys."""
    if not isinstance(data, dict):
        return _empty_schema()

    players = data.get("players")
    games = data.get("games")
    if not isinstance(players, dict):
        players = {}
    if not isinstance(games, list):
        games = []

    # Ensure per-player keys exist
    for pid, info in list(players.items()):
        if not isinstance(info, dict):
            players[pid] = {"name": pid, "wins": 0, "losses": 0}
        else:
            info.setdefault("name", pid)
            info.setdefault("wins", 0)
            info.setdefault("losses", 0)

    return {"players": players, "games": games}


class HighScore:
    """
    JSON-backed high score store.

    - If no path is provided, we use the package default file but we always
      start from a fresh empty schema to avoid test pollution from old data.
    """

    def __init__(self, path: Path | str | None = None) -> None:
        # Default path inside package
        default_path = Path(__file__).with_name("data").joinpath("highscores.json")

        if path is None:
            # Use default file but start clean every time
            self.path = default_path
            self.data = _empty_schema()
            self._write()
        else:
            self.path = Path(path)
            if self.path.exists():
                self.data = self._read()
            else:
                self.data = _empty_schema()
                self._write()

    # ---------- I/O ----------
    def _read(self) -> Dict[str, Any]:
        if not self.path.exists():
            return _empty_schema()
        try:
            with self.path.open("r", encoding="utf-8") as f:
                raw = json.load(f)
        except Exception:
            return _empty_schema()
        return _normalize_schema(raw)

    def _write(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    # ---------- Players ----------
    def register_player(self, name: str) -> str:
        """
        Register a player if missing; idempotent and case-insensitive.
        Keeps the original display name casing on re-registration.
        """
        pid = _canonical(name)
        if pid in self.data["players"]:
            # Do NOT change display name if the only difference is casing.
            # (If you want an actual rename, use rename_player.)
            return pid

        self.data["players"][pid] = {"name": name, "wins": 0, "losses": 0}
        self._write()
        return pid

    def rename_player(self, player_id: str, new_name: str) -> None:
        """
        Rename the display name for an existing player.
        Reject if the target canonical id belongs to another player.
        """
        pid = _canonical(player_id)
        if pid not in self.data["players"]:
            raise ValueError("Unknown player")

        new_pid = _canonical(new_name)
        if new_pid in self.data["players"] and new_pid != pid:
            # Cannot rename to another player's canonical id
            raise ValueError("Target name already exists")

        # Keep same pid; update display name only
        self.data["players"][pid]["name"] = new_name
        self._write()

    # ---------- Games / Results ----------
    def record_result(self, p1: str, p2: str, *args, **kwargs) -> None:
        """
        Record a game result between p1 and p2.

        Accepted forms:
          record_result(p1, p2)
          record_result(p1, p2, winner="alice", score_for=42, ...)
          record_result(p1, p2, {"winner": "alice", "score_for": 42, ...})
        Default winner (if omitted) = p1.
        """
        # Support dict payload as first *args
        if args and isinstance(args[0], dict):
            payload: Dict[str, Any] = args[0]
        else:
            payload = kwargs

        pid1 = _canonical(p1)
        pid2 = _canonical(p2)
        if pid1 == pid2:
            raise ValueError("Players must be different")
        if pid1 not in self.data["players"] or pid2 not in self.data["players"]:
            raise KeyError("Unknown player id")

        win_raw = payload.get("winner", pid1)
        win_pid = _canonical(win_raw)
        if win_pid not in (pid1, pid2):
            raise ValueError("Winner must be one of the players")
        lose_pid = pid2 if win_pid == pid1 else pid1

        score_for = int(payload.get("score_for", 0))
        score_against = int(payload.get("score_against", 0))
        duration_sec = int(payload.get("duration_sec", 0))

        # Update tallies
        self.data["players"][win_pid]["wins"] += 1
        self.data["players"][lose_pid]["losses"] += 1

        # Build record
        rec = GameRecord(
            p1=pid1,
            p2=pid2,
            winner=win_pid,
            score_for=score_for,
            score_against=score_against,
            duration_sec=duration_sec,
            when_utc=datetime.now(UTC).isoformat(timespec="seconds") + "Z",
        )
        rec_dict = asdict(rec)
        rec_dict["loser"] = lose_pid
        rec_dict["timestamp"] = rec_dict["when_utc"]  # compatibility

        self.data["games"].append(rec_dict)
        self._write()

    # Backwards-compat helpers
    def add_game(
        self,
        player1: str,
        player2: str,
        winner: str,
        score_for: int,
        score_against: int,
        duration_sec: int,
    ) -> None:
        self.record_result(
            player1,
            player2,
            winner=winner,
            score_for=score_for,
            score_against=score_against,
            duration_sec=duration_sec,
        )

    def add_result(self, *args, **kwargs) -> None:
        self.record_result(*args, **kwargs)

    # ---------- Views ----------
    def table(self) -> List[Tuple[str, str, int, int]]:
        """
        Return rows sorted as:
          - wins DESC
          - losses ASC
          - name (case-insensitive) ASC
        Each row is: (pid, display_name, wins, losses)
        """
        rows: List[Tuple[str, str, int, int]] = []
        for pid, info in self.data["players"].items():
            name = str(info.get("name", pid))
            wins = int(info.get("wins", 0))
            losses = int(info.get("losses", 0))
            rows.append((pid, name, wins, losses))

        rows.sort(key=lambda r: (-r[2], r[3], r[1].lower()))
        return rows

    # ---------- Misc ----------
    def reset(self) -> None:
        self.data = _empty_schema()
        self._write()

    def save(self) -> None:
        """Persist to disk explicitly."""
        self._write()
