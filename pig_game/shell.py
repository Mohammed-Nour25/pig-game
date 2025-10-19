# pig_game/shell.py
from __future__ import annotations
import argparse
import sys
import time

from pig_game.game import Game
from pig_game.intelligence import Intelligence
from pig_game.highscore import HighScoreStore, make_entry


def _game_over(g: Game) -> bool:
    """Return True if either player has won (by API or by reaching goal)."""
    try:
        if g.is_winner(0) or g.is_winner(1):
            return True
    except Exception:
        pass
    try:
        return any(s >= g.goal for s in g.scores)
    except Exception:
        return False


def _winner_index(g: Game) -> int | None:
    """Return 0 if Player 1 wins, 1 if Player 2 wins, else None."""
    try:
        if g.is_winner(0):
            return 0
        if g.is_winner(1):
            return 1
    except Exception:
        pass
    try:
        if g.scores[0] >= g.goal or g.scores[1] >= g.goal:
            return 0 if g.scores[0] >= g.scores[1] else 1
    except Exception:
        pass
    return None


def play_vs_cpu(player_name: str, level: str, store: HighScoreStore) -> int:
    """
    Human (Player 1) vs CPU (Player 2) using your Game API:
      - g.active_index (0 or 1), g.active / g.waiting labels
      - g.scores: [p1_total, p2_total]
      - g.turn_total: current turn points
      - g.roll() -> int, g.hold() -> None
      - g.is_winner(player_index: Optional[int]) -> bool
    Records a HighScore after the game ends (unless user quits).
    """
    g = Game()
    ai = Intelligence(level=level)
    started = time.time()
    user_quit = False
    record_result = True  # If the user quits, we'll set this to False.

    try:
        while not _game_over(g):
            human_total, cpu_total = g.scores[0], g.scores[1]
            turn_points = g.turn_total
            current_idx = g.active_index  # 0 = human, 1 = cpu

            if current_idx == 0:
                # Human turn
                print(f"\nYour turn, {player_name} — You: {human_total} | CPU: {cpu_total} | Turn: {turn_points}")
                cmd = input("[r=roll, h=hold, q=quit] > ").strip().lower()
                if cmd == "q":
                    print("Exiting game…")
                    user_quit = True
                    record_result = False  # do not compute win/lose or record highscores
                    break
                elif cmd == "r":
                    die = g.roll()
                    if die == 1:
                        # Bust: Game switches turn internally; turn_total reset to 0
                        print("🎲 You rolled 1 — turn lost.")
                    else:
                        print(f"🎲 You rolled {die}. Turn points: {g.turn_total}")
                elif cmd == "h":
                    g.hold()
                    print(f"You held. Your total is now {g.scores[0]}.")
                else:
                    print("Invalid command. Use r/h/q.")
                    continue
            else:
                # CPU turn
                print(f"\nCPU turn — CPU: {cpu_total} | You: {human_total} | Turn: {turn_points}")
                # Decision via Intelligence.should_hold()
                if ai.should_hold(g.turn_total, cpu_total, human_total):
                    g.hold()
                    print(f"🤖 CPU holds. CPU total: {g.scores[1]}")
                else:
                    die = g.roll()
                    if die == 1:
                        print("🤖 CPU rolled 1 — CPU loses its turn points.")
                    else:
                        print(f"🤖 CPU rolled {die}. CPU turn points: {g.turn_total}")

        # Game ended — compute result or handle quit
        duration = int(time.time() - started)
        human, cpu = g.scores[0], g.scores[1]

        # If user quit, do not print win/lose nor record highscores.
        if user_quit and not record_result:
            print("\n" + "—" * 40)
            print(f"Game aborted. Final snapshot ⇒ {player_name}: {human} | CPU: {cpu}")
            print("Result not recorded.")
            return 0

        # Otherwise, compute and print result, then record.
        winner_idx = _winner_index(g)
        if winner_idx is None:
            # Fallback by totals
            winner_idx = 0 if human >= cpu else 1

        result = "win" if winner_idx == 0 else "lose"
        score_for, score_against = (human, cpu) if result == "win" else (cpu, human)

        print("\n" + "—" * 40)
        print(f"Final Score ⇒ {player_name}: {human} | CPU: {cpu}")
        print("🎉 You win!" if result == "win" else "💀 You lose!")

        # Record HighScore safely
        try:
            store.add(make_entry(
                player=player_name,
                opponent="CPU",
                result=result,
                score_for=score_for,
                score_against=score_against,
                duration_sec=duration,
            ))
        except Exception as ex:
            print(f"Warning: failed to record HighScore ({ex})")

        return 0
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        return 130
    except Exception as ex:
        print(f"Unexpected error during game: {ex}")
        return 1


def show_highscores(limit: int, store: HighScoreStore) -> int:
    """Print a small HighScore table. Be polite if empty."""
    try:
        rows = store.top(limit)
        if not rows:
            print("No highscores yet. Play a game first, then try `pig high`.")
            return 0
        print(f"{'Player':<14} {'Vs':<6} {'Result':<6} {'For':>4} {'Against':>7} {'Duration(s)':>11}  {'When(UTC)'}")
        print("-" * 80)
        for r in rows:
            print(f"{r.player:<14} {'CPU':<6} {r.result:<6} {r.score_for:>4} {r.score_against:>7} {r.duration_sec:>11}  {r.when_utc}")
        return 0
    except Exception as ex:
        print(f"Failed to show highscores: {ex}")
        return 1


def build_parser() -> argparse.ArgumentParser:
    """
    Subcommands:
      - ai   : play vs CPU
      - high : show highscores
    """
    parser = argparse.ArgumentParser(
        prog="pig",
        description="Pig Game CLI — play vs CPU and view highscores.",
    )
    sub = parser.add_subparsers(dest="command")

    p_ai = sub.add_parser("ai", help="Play vs the computer (CPU).")
    p_ai.add_argument("--player", "-p", default="Player", help="Your displayed player name.")
    p_ai.add_argument("--level", "-l", default="normal", choices=["easy", "normal", "smart"], help="CPU intelligence level.")
    p_ai.set_defaults(cmd="ai")

    p_high = sub.add_parser("high", help="Show HighScore table.")
    p_high.add_argument("--limit", "-n", type=int, default=10, help="Max rows to show.")
    p_high.set_defaults(cmd="high")

    return parser


def main(argv: list[str] | None = None) -> int:
    store = HighScoreStore()
    parser = build_parser()
    args = parser.parse_args(argv)

    if not getattr(args, "cmd", None):
        parser.print_help(sys.stderr)
        print("\nExamples:\n  pig ai --player Mohammed --level normal\n  pig high --limit 10\n")
        return 2

    try:
        if args.cmd == "ai":
            return play_vs_cpu(args.player, args.level, store)
        elif args.cmd == "high":
            return show_highscores(args.limit, store)
        else:
            parser.print_help(sys.stderr)
            return 2
    except SystemExit as se:
        return int(se.code) if isinstance(se.code, int) else 1
    except Exception as ex:
        print(f"Unexpected CLI error: {ex}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
