"""Simple text-based CLI for the Pig game using Python's cmd module."""

from __future__ import annotations

import cmd
from typing import Optional

try:
    # Game is expected to be implemented in pig_game.game later.
    from pig_game.game import Game  # type: ignore
except Exception:
    Game = None  # type: ignore


RULES = (
    "Pig — Rules:\n"
    "- Players take turns rolling one die.\n"
    "- Add roll to turn points. If you roll 1, you bust (turn points = 0) and switch turn.\n"
    "- 'hold' banks turn points into total score and passes the turn.\n"
    "- First to reach the goal (default 100) wins.\n"
    "- 'cheat' adds +90 for quick testing.\n"
)


# ---------------- helpers (generic getters) ----------------
def _safe_get(obj, *names, default=None):
    """Try multiple attribute names or callables and return the first non-None value."""
    for name in names:
        if hasattr(obj, name):
            val = getattr(obj, name)
            try:
                return val() if callable(val) else val
            except Exception:
                continue
    return default


def _as_int(x, default=0):
    """Cast to int, or return default on failure."""
    try:
        return int(x)
    except Exception:
        return default


class PigShell(cmd.Cmd):
    """Command-line shell for the Pig game."""

    intro = "Welcome to Pig! Type 'help' or '?' for commands.\n"
    prompt = "(pig) "

    def __init__(self) -> None:
        super().__init__()
        self.game: Optional[Game] = None  # type: ignore[assignment]

    # ---------------- helpers ----------------
    def _need_game(self) -> bool:
        """Ensure a game instance exists before running a command."""
        if self.game is None:
            print("No game started. Use: start [goal]")
            return False
        return True

    def _render_status(self) -> None:
        """Pretty status: players, scores, turn points, goal, active arrow, winner if any."""
        g = self.game
        if g is None:
            print("No game started. Use: start [goal]")
            return

        players = _safe_get(g, "players") or []
        active = _as_int(_safe_get(g, "active_player", "active_index", default=0))
        turn_points = _as_int(_safe_get(g, "turn_points", default=0))
        goal = _as_int(_safe_get(g, "goal_score", "goal", default=100))
        winner = _safe_get(g, "winner", "get_winner")  # could be idx/name/player/None

        lines = [f"Goal: {goal}"]
        for i, p in enumerate(players):
            name = _safe_get(p, "name", default=f"Player{i+1}")
            total = _as_int(_safe_get(p, "score", "total_score", default=0))
            mark = "←" if (i == active or bool(_safe_get(p, "is_active", default=False))) else " "
            lines.append(f"{mark} {name:12s} total={total}")
        lines.append(f"Turn points: {turn_points}")
        print("\n".join(lines))

        if winner:
            # winner could be an index, a player object, or a name/id
            if isinstance(winner, int) and 0 <= winner < len(players):
                win_name = _safe_get(players[winner], "name", default=f"Player{winner+1}")
            elif hasattr(winner, "name"):
                win_name = _safe_get(winner, "name", default=str(winner))
            else:
                win_name = str(winner)
            print(f"🏆 Winner: {win_name}! Type 'start' to play again.")

    def _maybe_announce_winner(self) -> None:
        g = self.game
        if g is None:
            return
        if _safe_get(g, "winner", "get_winner"):
            self._render_status()

    # ---------------- commands ----------------
    def do_start(self, arg: str) -> None:
        """start [goal] -> start a new game (default 100)."""
        if Game is None:
            print("Game class not available yet.")
            return

        # parse goal
        goal = 100
        s = arg.strip()
        if s:
            try:
                goal = int(s)
                if goal < 1:
                    raise ValueError
            except ValueError:
                print("Goal must be a positive integer. Using 100.")
                goal = 100

        # try to build Game safely
        try:
            # preferred: keyword arg
            self.game = Game(goal_score=goal)  # type: ignore[call-arg]
        except TypeError:
            # fallback: no-arg constructor, then set attribute if it exists
            try:
                self.game = Game()  # type: ignore[call-arg]
                if hasattr(self.game, "goal_score"):
                    setattr(self.game, "goal_score", goal)  # type: ignore[attr-defined]
            except NotImplementedError:
                print("Game core is not implemented yet (M1). Try again later.")
                self.game = None
                return
            except Exception as exc:
                print(f"Could not start game: {exc}")
                self.game = None
                return
        except NotImplementedError:
            print("Game core is not implemented yet (M1). Try again later.")
            self.game = None
            return
        except Exception as exc:
            print(f"Could not start game: {exc}")
            self.game = None
            return

        print(f"New game started. Goal = {goal}.")
        self.do_status("")

    def do_status(self, _: str) -> None:
        """status -> show scores and current turn."""
        if not self._need_game():
            return
        try:
            self._render_status()
        except Exception:
            print("Game is running, but status will improve once Game is finalized.")

    def do_rules(self, _: str) -> None:
        """rules -> show Pig rules."""
        print(RULES)

    def do_quit(self, _: str) -> bool:
        """quit -> exit the game."""
        print("Bye!")
        return True

    # Allow Ctrl-D / Ctrl-Z to quit
    do_EOF = do_quit

    # ---- gameplay commands (safe wiring; won't crash if Game isn't ready) ----
    def do_roll(self, _: str) -> None:
        """roll -> roll the dice for the current player."""
        if not self._need_game():
            return
        try:
            if not hasattr(self.game, "roll"):
                print("Game.roll() is missing. Please implement it in the Game class.")
                return
            result = self.game.roll()  # type: ignore[attr-defined]
            if result is not None:
                print(f"Rolled: {result}")
        except NotImplementedError:
            print("roll() is not implemented in Game yet.")
            return
        except Exception as exc:
            print(f"roll failed: {exc}")
            return

        self._render_status()
        self._maybe_announce_winner()

    def do_hold(self, _: str) -> None:
        """hold -> bank turn points and switch player."""
        if not self._need_game():
            return

        try:
            if not hasattr(self.game, "hold"):
                print("Game class missing 'hold' method. Implement it first.")
                return
            self.game.hold()  # type: ignore[attr-defined]
            print("Points banked. Turn passed to next player.")
        except NotImplementedError:
            print("hold() is not implemented in Game yet.")
        except Exception as exc:
            print(f"hold failed: {exc}")

        self._render_status()
        self._maybe_announce_winner()

    def do_cheat(self, _: str) -> None:
        """cheat -> add +90 to active player (testing)."""
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
                        p.score += 90  # type: ignore[attr-defined]
                    elif hasattr(p, "total_score"):
                        p.total_score += 90  # type: ignore[attr-defined]
            print("+90 applied.")
        except Exception as exc:
            print(f"cheat failed: {exc}")

        self._render_status()
        self._maybe_announce_winner()

    def do_name(self, arg: str) -> None:
        """name <new_name> -> change active player's name."""
        if not self._need_game():
            return

        new = arg.strip()
        if not new:
            print("Usage: name <new_name>")
            return

        try:
            players = _safe_get(self.game, "players") or []
            active = _as_int(_safe_get(self.game, "active_player", "active_index", default=0))
            if 0 <= int(active) < len(players):
                setattr(players[int(active)], "name", new)  # type: ignore[attr-defined]
                print(f"Name set to '{new}'")
            else:
                print("No active player index available.")
        except Exception as exc:
            print(f"name failed: {exc}")

        self._render_status()

    # --------------- misc ---------------
    def default(self, line: str) -> None:
        """Handle unknown commands gracefully."""
        print(f"Unknown command: {line!r}. Try 'help'.")

    def emptyline(self) -> None:
        """Do nothing on empty line (avoid repeating the last command)."""
        pass


def main() -> None:
    """Entry point to start the PigShell CLI loop."""
    PigShell().cmdloop()
