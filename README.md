# 🐷 Pig Game — Command-Line Interface (CLI)

The project includes a simple text-based command-line interface (CLI) for playing the **Pig game** interactively.

## ▶️ Run the CLI
You can start the CLI directly using Python:

```bash
python -m pig_game
```

This will open an interactive shell like:

```
Welcome to Pig! Type 'help' or '?' for commands.

(pig)
```

## 🧩 Available Commands
| Command | Description |
|----------|--------------|
| `start [goal]` | Start a new game (default goal = 100 points). |
| `roll` | Roll the die for the current player. |
| `hold` | Bank your current turn points and pass the turn. |
| `status` | Show scores and whose turn it is. |
| `name <new_name>` | Change the active player’s name. |
| `rules` | Display Pig game rules. |
| `cheat` | Add +90 points to active player (for testing). |
| `quit` / `Ctrl+D` | Exit the game. |

## 💡 Example Session
```
Welcome to Pig! Type 'help' or '?' for commands.

(pig) rules
Pig — Rules:
- Players take turns rolling one die.
- Add roll to turn points. If you roll 1, you bust (turn points = 0) and switch turn.
- 'hold' banks turn points into total score and passes the turn.
- First to reach the goal (default 100) wins.
- 'cheat' adds +90 for quick testing.

(pig) start
New game started. Goal = 100.
Player1 total=0
Player2 total=0
Turn points: 0

(pig) roll
roll is not implemented in Game yet.

(pig) quit
Bye!
```
