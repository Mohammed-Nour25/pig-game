from pathlib import Path
from pig_game.highscore import HighScore

def test_add_result_alias(tmp_path: Path):
    """Covers the add_result() alias that forwards to record_result()."""
    p = tmp_path / "hs.json"
    hs = HighScore(p)
    a = hs.register_player("Alice")
    b = hs.register_player("Bob")
    # Use alias to ensure it's included in coverage
    hs.add_result(a, b, winner=a, score_for=50, score_against=10, duration_sec=5)
    table = hs.table()
    stats = {pid: (w, l) for pid, name, w, l in table}
    assert stats[a][0] >= 1  # Alice won at least once via alias

def test_add_game_alias(tmp_path: Path):
    """Covers the add_game() alias that forwards to record_result()."""
    p = tmp_path / "hs2.json"
    hs = HighScore(p)
    a = hs.register_player("Alice")
    b = hs.register_player("Bob")
    # Use alias to ensure it's included in coverage
    hs.add_game(a, b, winner=b, score_for=60, score_against=30, duration_sec=7)
    table = hs.table()
    stats = {pid: (w, l) for pid, name, w, l in table}
    assert stats[b][0] >= 1  # Bob won at least once via alias
