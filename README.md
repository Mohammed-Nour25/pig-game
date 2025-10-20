# Pig Game — Command-Line Interface (CLI)

The project includes a polished **text-based command-line interface (CLI)** for playing the **Pig game** interactively.

---

## Run the CLI
You can start the CLI directly using Python:

```bash
python -m pig_game


```

This will open an interactive shell like:

```
Welcome to Pig! Type 'help' or '?' for available commands.

(pig)
```

##  Available Commands
| Command | Description |
|----------|--------------|
| `start [goal]` | Start a new game (default goal = 100 points). |
| `roll` | Roll the die for the current player. |
| `hold` | Bank your current turn points and pass the turn. |
| `status` | Show scores and whose turn it is. |
| `name <new_name>` | Change the active player’s name. |
| `rules` | Display Pig game rules. |
| `cheat` | Add +90 points to the active player (for quick testing). |
| `quit` / `Ctrl+D` | Exit the game. |

##  Example Session
```
Welcome to Pig! Type 'help' or '?' for commands.

```
 Welcome to Pig! Type 'help' or '?' for available commands.

(pig) start
 New game started. Goal = 100.

════════════════════════════════════════
 Goal: 100 |  Turn points: 0
────────────────────────────────────────
   Player1      | total = 0
   Player2      | total = 0
════════════════════════════════════════

(pig) roll
 Rolled: 1 💥 Bust! Switching turn…

(pig) hold
💾 Points banked. Switching turn…

(pig) cheat
✨ +90 applied.

(pig) name Ali
✅ Name set to 'Ali'

(pig) status
════════════════════════════════════════
🎯 Goal: 100 | 🎲 Turn points: 0
────────────────────────────────────────
👉 Ali          | total = 90
   Player2      | total = 0
════════════════════════════════════════

(pig) quit
👋 Bye!
```

---

## 🧠 Notes
- Handles **invalid input gracefully** (e.g., typing `roll` before `start` shows a friendly warning instead of crashing).  
- Uses Python’s built-in [`cmd`](https://docs.python.org/3/library/cmd.html) module for an interactive shell experience.  
- Supports safe integration with partially implemented game logic.  
- Displays scores, turn points, and active player using clean and formatted output.  

---

## 🧪 Development Summary (M1-3)

### Summary
- Enhanced CLI message clarity when a user tries to run a command before starting a game.  
- Ensured invalid input handling flows gracefully without crashes.  
- Added color-coded and emoji-based feedback for better user experience.

### Details
✅ Added clearer prompt for `No game started`  
✅ Verified graceful behavior for invalid commands and empty input  
✅ Completed final part of **M1-3** ("Display scores, handle invalid input gracefully")

### Testing
Run:
```bash
python -m pig_game
```

## UML Diagrams

We generate class and package diagrams using `pyreverse` (from `pylint`) and Graphviz.

### Prerequisites
Make sure you have:
- Graphviz installed (`dot -V` should work)
- `pylint` and `graphviz` installed in your Python environment:
  ```bash
  pip install pylint graphviz

### Generate the diagrams
To generate UML diagrams automatically, run:
```bash
make uml
Then try:
```bash
roll
hold
cheat
status
quit
```

Expected:
- Friendly ⚠️ messages when game not started.  
- No crashes or errors.  
- Smooth user experience with clear feedback.

---

## 🕹️ Command Line Interface (AI + HighScore Integration)

The **Pig Game** also supports playing against an **AI opponent** and viewing saved **HighScores**.

### ▶️ Start a Game vs CPU

```bash
python -m pig_game.shell ai --player "Mohammed" --level normal
```

**Options:**

| Option | Description | Default |
|:--------|:-------------|:----------|
| `--player`, `-p` | Your displayed name | `"Player"` |
| `--level`, `-l` | CPU difficulty (`easy`, `normal`, `smart`) | `normal` |

**Example Gameplay:**

```
Your turn, Mohammed — You: 0 | CPU: 0 | Turn: 0
[r=roll, h=hold, q=quit] > r
🎲 You rolled 4. Turn points: 4
[r=roll, h=hold, q=quit] > h
You held. Your total is now 4.

CPU turn — CPU: 0 | You: 4 | Turn: 0
🤖 CPU rolled 6. CPU turn points: 6
🤖 CPU holds. CPU total: 6
```

At the end of the game, the system automatically records the result in the **HighScore** table (unless the player quits using `q`).

---

### 🏆 View HighScores

To view recorded results:

```bash
python -m pig_game.shell high --limit 10
```

Example output:

```
Player         Vs     Result  For Against Duration(s)  When(UTC)
--------------------------------------------------------------------------------
Mohammed       CPU    win     150      64         250  2025-10-15T22:32:22Z
```

**Tip:** Use `--limit` to change how many rows are displayed.

---

### 💡 Notes
- The game’s CPU uses `Intelligence.should_hold()` to decide whether to continue rolling or hold.
- High scores are stored locally at `~/.pig_highscores.json`.
- Invalid commands are handled safely (e.g., if the user types anything other than `r`, `h`, or `q`).

---

## 👨‍💻 Contributors
- **Mohammed Nour** — CLI implementation, AI & HighScore integration, error handling, and documentation.

---

## 📄 License
This project is licensed under the terms described in [LICENSE.md](LICENSE.md).



## Regenerating API Documentation

This project uses [pdoc](https://pdoc.dev/) to generate API documentation for the 
`pig_game` package.

### Steps to regenerate docs

1. Make sure `pdoc` is installed:
```bash
python3 -m pip install pdoc

