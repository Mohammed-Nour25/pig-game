"""HighScore JSON storage (skeleton).
TODO (M2):
- File: pig_game/data/highscores.json (create folder if missing)
- players: { pid: {name, plays, wins, losses, last_updated} }
- games: [{winner_pid, loser_pid, date}]
- Facade: register_player(name)->pid, rename_player(pid,new_name), record_result(...), table()
- ≥90% coverage, docstrings
"""

from __future__ import annotations

class HighScore:  # pragma: no cover
    """HighScore facade (skeleton)."""
    def __init__(self, path: str | None = None) -> None:
        raise NotImplementedError("Implement HighScore for M2")

    def register_player(self, name: str) -> str:
        raise NotImplementedError("Implement register_player for M2")

    def rename_player(self, pid: str, new_name: str) -> None:
        raise NotImplementedError("Implement rename_player for M2")

    def record_result(self, winner_pid: str, loser_pid: str) -> None:
        raise NotImplementedError("Implement record_result for M2")

    def table(self):
        raise NotImplementedError("Implement table for M2")
