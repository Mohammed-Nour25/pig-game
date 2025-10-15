# pig_game/highscore.py
from __future__ import annotations
import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List

DEFAULT_STORE = os.path.join(os.path.expanduser("~"), ".pig_highscores.json")

@dataclass
class HighScoreEntry:
    player: str
    opponent: str
    result: str        # "win" or "lose"
    score_for: int
    score_against: int
    duration_sec: int
    when_utc: str      # ISO timestamp

class HighScoreStore:
    """
    Very small JSON-based highscore store suitable for a CLI app.
    """
    def __init__(self, path: str = DEFAULT_STORE) -> None:
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _read_all(self) -> List[HighScoreEntry]:
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [HighScoreEntry(**row) for row in data]

    def _write_all(self, entries: List[HighScoreEntry]) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([asdict(e) for e in entries], f, ensure_ascii=False, indent=2)

    def add(self, entry: HighScoreEntry) -> None:
        entries = self._read_all()
        entries.append(entry)
        self._write_all(entries)

    def top(self, limit: int = 10) -> List[HighScoreEntry]:
        """
        Sort by: wins first, then higher 'score_for', then shorter duration.
        """
        entries = self._read_all()
        entries.sort(key=lambda e: (-int(e.result == "win"), -e.score_for, e.duration_sec))
        return entries[:limit]

def make_entry(player: str, opponent: str, result: str, score_for: int, score_against: int, duration_sec: int) -> HighScoreEntry:
    return HighScoreEntry(
        player=player,
        opponent=opponent,
        result=result,
        score_for=score_for,
        score_against=score_against,
        duration_sec=duration_sec,
        when_utc=datetime.utcnow().isoformat(timespec="seconds") + "Z",
    )
