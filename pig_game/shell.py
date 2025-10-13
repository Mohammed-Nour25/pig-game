"""Simple text-based CLI for the Pig game using Python's cmd module."""

import cmd
from typing import Optional

try:
    from pig_game.game import Game  # type: ignore
except Exception:
    Game = None  # type: ignore


RULES = (
    "🐷 Pig — Rules:\n"
    "- Players take turns rolling one die.\n"
    "- Add roll to turn points. If you roll 1, you bust (turn points = 0) and switch turn.\n"
    "- 'hold' banks turn points into total score and passes the turn.\n"
    "- First to reach the goal (default 100) wins.\n"
    "- 'cheat' adds +90 for quick testing.\n"
)


def _safe_get(obj, *names, default=None):
    """Try multiple attribute names and return the first valid value."""
    for name in names:
        if hasattr(obj, name):
            val = getattr(obj, name)
            try:
                return val() if callable(val) else val
            except Exception:
                continue
    return default


def _as_int(x, default=0):
    """Cast safely to int, return default on failure."""
    try:
        return int(x)
    except Exception:
        return default


def _line(char="─", n=40) -> str:
    """Return a line separator of given length."""
    return char * n


class PigShell(cmd.Cmd):
    """Command-line shell for the Pig game."""

    intro = "🐷 Welcome to Pig! Type 'help' or '?' for available commands.\n"
    prompt = "(pig) "

    def __init__(self) -> None:
        super().__init__()
        self.game: Optional[Game] = None  # type: ignore[assignment]

    # ---------------- Helpers ----------------
    def _need_game(self) -> bool:
        """Check if a game exists before running a command."""
        if self.game is None:
            print("⚠️  No game started. Use: start [goal]")
            return False
        return True

    def _render_status(self) -> None:
        """Display a clean, readable status panel."""
        g = self.game
        if g is None:
            print("⚠️  No game started. Use: start [goal]")
            return

        players = _safe_get(g, "players") or []
        active = _as_int(_safe_get(g, "active_player", "active_index", default=0))
        turn_points = _as_int(_safe_get(g, "turn_points", default=0))
        goal = _as_int(_safe_get(g, "goal_score", "goal", default=100))
        winner = _safe_get(g, "winner", "get_winner")

        print(_line("═", 40))
        print(f"🎯 Goal: {goal} | 🎲 Turn points: {turn_points}")
 print("⚠️  No game started. Use: start [goal]")
 print("⚠️  No game started. Use: start [goal]")
        print(_line("─", 40))
        for i, p in enumerate(players):
            name = _safe_get(p, "name", default=f"Player{i+1}")
            total = _as_int(_safe_get(p, "score", "total_score", default=0))
            mark = "👉" if (i == active or bool(_safe_get(p, "is_active", default=False))) else "  "
            print(f"{mark} {name:<12} | total = {total}")
        print(_line("═", 40))

        if winner:
            if isinstance(winner, int) and 0 <= winner < len(players):
                win_name = _safe_get(players[winner], "name", default=f"Player{winner+1}")
            elif hasattr(winner, "name"):
                win_name = _safe_get(winner, "name", default=str(winner))
            else:
                win_name = str(winner)
            print(f"🏆 Winner: {win_name}! Type 'start' to play again.\n")

    # ---------------- Commands ----------------
    def do_start(self, arg: str) -> None:
        """start [goal] -> start a new game (default 100)."""
        if Game is None:
            print("❌ Game class not available yet.")
            return

        goal = 100
        s = arg.strip()
        if s:
            try:
                goal = int(s)
                if goal < 1:
                    raise ValueError
            except ValueError:
                print("⚠️  Goal must be a positive integer. Using 100.")
                goal = 100

        try:
            self.game = Game(goal_score=goal)  # type: ignore[call-arg]
        except TypeError:
            try:
                self.game = Game()  # type: ignore[call-arg]
                if hasattr(self.game, "goal_score"):
                    setattr(self.game, "goal_score", goal)
            except Exception as exc:
                print(f"❌ Could not start game: {exc}")
                self.game = None
                return
        except Exception as exc:
            print(f"❌ Could not start game: {exc}")
            self.game = None
            return

        print(f"✅ New game started. Goal = {goal}.\n")
        self._render_status()

    def do_status(self, _: str) -> None:
        """status -> show scores and current turn."""
        if self._need_game():
            self._render_status()

    def do_rules(self, _: str) -> None:
        """rules -> show Pig rules."""
        print(RULES)

    def do_quit(self, _: str) -> bool:
        """quit -> exit the game."""
        print("👋 Bye!")
        return True

    do_EOF = do_quit  # Ctrl-D / Ctrl-Z quits

    # ---- Gameplay Commands ----
    def do_roll(self, _: str) -> None:
        """roll -> roll the dice for the current player."""
        if not self._need_game():
            return
        try:
            value = self.game.roll()  # type: ignore[attr-defined]
            if value == 1:
                print("🎲 Rolled: 1 → 💥 Bust! Switching turn…")
            else:
                print(f"🎲 Rolled: {value}")
        except Exception as exc:
            print(f"❌ roll failed: {exc}")
            return

        self._render_status()

    def do_hold(self, _: str) -> None:
        """hold -> bank turn points and switch player."""
        if not self._need_game():
            return
        try:
            result = self.game.hold()  # type: ignore[attr-defined]
            if result == "win":
                print("🏆 Winner detected! 🎉")
            else:
                print("💾 Points banked. Switching turn…")
        except Exception as exc:
            print(f"❌ hold failed: {exc}")

        self._render_status()

    def do_cheat(self, _: str) -> None:
        """cheat -> add +90 to active player (for testing)."""
        if not self._need_game():
            return

        g = self.game
        try:
            if hasattr(g, "cheat"):
                g.cheat(90)  # type: ignore[attr-defined]
            else:
                players = _safe_get(g, "players") or []
                active = _as_int(_safe_get(g, "active_player", "active_index", default=0))
                if 0 <= int(active) < len(players):
                    p = players[int(active)]
                    if hasattr(p, "score"):
                        p.score += 90
                    elif hasattr(p, "total_score"):
                        p.total_score += 90
            print("✨ +90 applied.")
        except Exception as exc:
            print(f"❌ cheat failed: {exc}")

        self._render_status()

    def do_name(self, arg: str) -> None:
        """name <new_name> -> change active player's name."""
        if not self._need_game():
            return

        new = arg.strip()
        if not new:
            print("⚠️  Usage: name <new_name>")
            return

        try:
            players = _safe_get(self.game, "players") or []
            active = _as_int(_safe_get(self.game, "active_player", "active_index", default=0))
            if 0 <= int(active) < len(players):
                setattr(players[int(active)], "name", new)
                print(f"✅ Name set to '{new}'")
            else:
                print("⚠️  No active player index available.")
        except Exception as exc:
            print(f"❌ name failed: {exc}")

        self._render_status()

    # --------------- Misc ---------------
    def default(self, line: str) -> None:
        """Handle unknown commands gracefully."""
        print(f"⚠️  Unknown command: {line!r}. Try 'help'.")

    def emptyline(self) -> None:
        """Ignore empty lines (avoid repeating last command)."""
        pass


def main() -> None:
    """Entry point to start the PigShell CLI loop."""
    PigShell().cmdloop()
