# 🐷 Pig Game — Command-Line Interface (CLI)

The project includes a polished **text-based command-line interface (CLI)** for playing the **Pig game** interactively.

---

## ▶️ Run the CLI
You can start the CLI directly using Python:

```bash
python -m pig_game
```

This will open an interactive shell like:

```
🐷 Welcome to Pig! Type 'help' or '?' for available commands.

(pig)
```

---

## 🧩 Available Commands

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

---

## 💡 Example Session

```
🐷 Welcome to Pig! Type 'help' or '?' for available commands.

(pig) start
✅ New game started. Goal = 100.

════════════════════════════════════════
🎯 Goal: 100 | 🎲 Turn points: 0
────────────────────────────────────────
👉 Player1      | total = 0
   Player2      | total = 0
════════════════════════════════════════

(pig) roll
🎲 Rolled: 1 → 💥 Bust! Switching turn…

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

## 👨‍💻 Contributors
- **Mohammed Nour** — CLI implementation, error handling, and README documentation.
