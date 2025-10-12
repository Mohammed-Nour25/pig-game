"""Simple text-based CLI for the Pig game using Python's cmd."""

import cmd

try:
    # توقع أن Game موجود لاحقًا في pig_game.game
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


class PigShell(cmd.Cmd):
    intro = "Welcome to Pig! Type 'help' or '?' for commands.\n"
    prompt = "(pig) "

    def __init__(self) -> None:
        super().__init__()
        self.game = None  # type: ignore

    # -------- basic helpers --------
    def _need_game(self) -> bool:
        if self.game is None:
            print("No game started. Use: start [goal]")
            return False
        return True

    # -------- commands --------
    def do_start(self, arg: str) -> None:
        """start [goal]  -> start a new game (default 100)."""
        if Game is None:
            print("Game class not available yet.")
            return

        # goal parsing
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

        # try to build Game
        try:
            self.game = Game(goal_score=goal)  # type: ignore[call-arg]
        except TypeError:
            self.game = Game()  # type: ignore[call-arg]
            if hasattr(self.game, "goal_score"):
                self.game.goal_score = goal  # type: ignore[attr-defined]

        print(f"New game started. Goal = {goal}.")
        self.do_status("")

    def do_status(self, _: str) -> None:
        """status  -> show scores and current turn."""
        if not self._need_game():
            return

        g = self.game
        try:
            players = getattr(g, "players", [])
            active = getattr(g, "active_player", None) or getattr(g, "active_index", 0)
            turn_points = getattr(g, "turn_points", 0)

            for i, p in enumerate(players):
                name = getattr(p, "name", f"Player{i+1}")
                total = getattr(p, "score", getattr(p, "total_score", 0))
                marker = "<-" if (i == active or getattr(p, "is_active", False)) else "  "
                print(f"{marker} {name:12s} total={total}")
            print(f"Turn points: {turn_points}")
        except Exception:
            print("Game is running, but status view will be better once Game is finalized.")

    def do_rules(self, _: str) -> None:
        """rules   -> show Pig rules."""
        print(RULES)

    def do_quit(self, _: str) -> bool:
        """quit    -> exit the game."""
        print("Bye!")
        return True

    # Ctrl-D/Ctrl-Z to quit
    do_EOF = do_quit

    # The following will work once Game methods exist; handled safely if not.
    def do_roll(self, _: str) -> None:
        """roll    -> roll dice for current player."""
        if not self._need_game():
            return
        try:
            res = self.game.roll()  # type: ignore[operator]
            if res is not None:
                print(f"Rolled: {res}")
        except Exception as e:
            print(f"roll failed: {e}")
        self.do_status("")

    def do_hold(self, _: str) -> None:
        """hold    -> bank turn points and switch player."""
        if not self._need_game():
            return
        try:
            self.game.hold()  # type: ignore[operator]
        except Exception as e:
            print(f"hold failed: {e}")
        self.do_status("")

    def do_cheat(self, _: str) -> None:
        """cheat   -> add +90 to active player (testing)."""
        if not self._need_game():
            return
        g = self.game
        try:
            if hasattr(g, "cheat"):
                g.cheat(90)  # type: ignore[attr-defined]
            else:
                players = getattr(g, "players", [])
                active = getattr(g, "active_player", None) or getattr(g, "active_index", 0)
                if 0 <= int(active) < len(players):
                    p = players[int(active)]
                    if hasattr(p, "score"):
                        p.score += 90  # type: ignore[attr-defined]
                    elif hasattr(p, "total_score"):
                        p.total_score += 90  # type: ignore[attr-defined]
            print("+90 applied.")
        except Exception as e:
            print(f"cheat failed: {e}")
        self.do_status("")

    def do_name(self, arg: str) -> None:
        """name <new_name>  -> change active player's name."""
        if not self._need_game():
            return
        new = arg.strip()
        if not new:
            print("Usage: name <new_name>")
            return
        try:
            players = getattr(self.game, "players", [])
            active = getattr(self.game, "active_player", None) or getattr(self.game, "active_index", 0)
            if 0 <= int(active) < len(players):
                players[int(active)].name = new  # type: ignore[attr-defined]
                print(f"Name set to '{new}'")
            else:
                print("No active player index available.")
        except Exception as e:
            print(f"name failed: {e}")
        self.do_status("")

    # unknown command
    def default(self, line: str) -> None:
        print(f"Unknown command: {line!r}. Try 'help'.")

    # ignore empty line (don't repeat last command)
    def emptyline(self):
        pass


def main() -> None:
    PigShell().cmdloop()
