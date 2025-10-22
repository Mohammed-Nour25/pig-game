import json
from pathlib import Path

import pytest

from pig_game.highscore import HighScore


# --- Fixture: isolated HighScore using a temp JSON path ---
@pytest.fixture()
def hs(tmp_path: Path) -> HighScore:
    path = tmp_path / "highscores.json"
    return HighScore(path)


def read_json(p: Path) -> dict:
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


# 1) creation/load should create file and minimal schema
def test_load_creates_file_if_missing(tmp_path: Path):
    p = tmp_path / "hs.json"
    assert not p.exists()
    h = HighScore(p)
    assert p.exists()
    data = read_json(p)
    assert "players" in data and isinstance(data["players"], dict)
    assert "games" in data and isinstance(data["games"], list)


# 2) register adds new player, returns same pid if name (case-insensitive) repeats
def test_register_new_and_existing_case_insensitive(hs: HighScore):
    p1 = hs.register_player("Alice")
    p2 = hs.register_player("alice")  # same person, different case
    p3 = hs.register_player("Bob")
    assert p1 == p2
    assert p1 != p3
    assert hs.data["players"][p1]["name"] == "Alice"
    assert set(hs.data["players"].keys()) == {p1, p3}


# 3) rename works
def test_rename_player_success(hs: HighScore):
    p1 = hs.register_player("Alice")
    hs.rename_player(p1, "Alicia")
    assert hs.data["players"][p1]["name"] == "Alicia"


# 4) rename rejects duplicate name (case-insensitive)
def test_rename_player_conflict(hs: HighScore):
    p1 = hs.register_player("Alice")
    p2 = hs.register_player("Bob")
    with pytest.raises(ValueError):
        hs.rename_player(p1, "bob")  # already taken by p2


# 5) record_result updates counters and logs a game
def test_record_result_updates_stats_and_logs(hs: HighScore):
    p1 = hs.register_player("Alice")
    p2 = hs.register_player("Bob")
    hs.record_result(p1, p2)
    assert hs.data["players"][p1]["wins"] == 1
    assert hs.data["players"][p2]["losses"] == 1
    assert len(hs.data["games"]) == 1
    last = hs.data["games"][-1]
    assert last["winner"] == p1 and last["loser"] == p2
    assert "timestamp" in last


# 6) record_result validates IDs
def test_record_result_invalid_ids_raise(hs: HighScore):
    p1 = hs.register_player("Alice")
    with pytest.raises(KeyError):
        hs.record_result(p1, "p999")


# 7) record_result same IDs not allowed
def test_record_result_same_ids_raises(hs: HighScore):
    p1 = hs.register_player("Alice")
    with pytest.raises(ValueError):
        hs.record_result(p1, p1)


# 8) table sorting: wins desc, losses asc, name asc
def test_table_sorting_order(hs: HighScore):
    a = hs.register_player("Alice")
    b = hs.register_player("Bobby")
    c = hs.register_player("Charlie")

    # results: Alice 2-0, Charlie 1-1, Bobby 0-2
    hs.record_result(a, b)
    hs.record_result(c, b)
    hs.record_result(a, c)

    table = hs.table()
    # Expect order: Alice, Charlie, Bobby
    assert [row[1] for row in table] == ["Alice", "Charlie", "Bobby"]
    # And verify the numbers align
    by_pid = {pid: (w, l) for pid, _n, w, l in table}
    assert by_pid[a] == (2, 0)
    assert by_pid[c] == (1, 1)
    assert by_pid[b] == (0, 2)


# 9) persistence across runs (IDs and stats stable)
def test_persistence_across_runs(tmp_path: Path):
    p = tmp_path / "hs.json"
    h1 = HighScore(p)
    a = h1.register_player("Alice")
    b = h1.register_player("Bob")
    h1.record_result(a, b)
    h1.save()

    # new instance reading same file
    h2 = HighScore(p)
    assert a in h2.data["players"] and b in h2.data["players"]
    assert h2.data["players"][a]["wins"] == 1
    assert h2.data["players"][b]["losses"] == 1
    assert len(h2.data["games"]) == 1


# 10) schema normalization if file is missing keys or corrupted
def test_schema_normalization_missing_keys(tmp_path: Path):
    p = tmp_path / "hs.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    # Create a file with wrong structure
    with p.open("w", encoding="utf-8") as f:
        json.dump({"wrong": 1}, f)
    h = HighScore(p)
    assert "players" in h.data and isinstance(h.data["players"], dict)
    assert "games" in h.data and isinstance(h.data["games"], list)
