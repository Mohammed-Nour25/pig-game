# 🎲 Pig Game

A Python implementation of the Pig Game — a simple dice game built with 
modular, test-driven development.

---

## 📋 Table of Contents

- [Development and Testing](#development-and-testing)
- [Command-Line Interface (CLI)](#command-line-interface-cli)
- [AI & HighScore Features](#ai--highscore-features)
- [UML Diagrams](#uml-diagrams)
- [API Documentation](#api-documentation)
- [Contributors](#contributors)
- [License](#license)

---

## 🛠️ Development and Testing

This project uses a `Makefile` to simplify common development tasks.

### Setup

Install all required dependencies:

```bash
make install
```

This will install:
- Core game dependencies
- Development tools (`pylint`, `pdoc`, `pytest`)
- Documentation tools (`graphviz`)

---

## 🎮 Command-Line Interface (CLI)

The project includes a polished text-based command-line interface (CLI) for playing the Pig game interactively.

### Run the CLI

You can start the CLI directly using Python:

```bash
python -m pig_game
```

This will open an interactive shell:

```
Welcome to Pig! Type 'help' or '?' for available commands.

(pig) 
```

### Available Commands

| Command | Description |
|---------|-------------|
| `start [goal]` | Start a new game (default goal = 100 points). |
| `roll` | Roll the die for the current player. |
| `hold` | Bank your current turn points and pass the turn. |
| `status` | Show scores and whose turn it is. |
| `name <new_name>` | Change the active player's name. |
| `rules` | Display Pig game rules. |
| `cheat` | Add +90 points to the active player (for quick testing). |
| `quit` / Ctrl+D | Exit the game. |

### Example Session

```
Welcome to Pig! Type 'help' or '?' for available commands.

(pig) start
New game started. Goal = 100.

════════════════════════════════════════
Goal: 100 | Turn points: 0
────────────────────────────────────────
Player1 | total = 0
Player2 | total = 0
════════════════════════════════════════

(pig) roll
Rolled: 1
💥 Bust! Switching turn…

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
👉 Ali | total = 90
   Player2 | total = 0
════════════════════════════════════════

(pig) quit
👋 Bye!
```

### 🧠 Notes

- Handles **invalid input gracefully** (e.g., typing `roll` before `start` shows a friendly warning instead of crashing).  
- Uses Python's built-in [`cmd`](https://docs.python.org/3/library/cmd.html) module for an interactive shell experience.  
- Supports safe integration with partially implemented game logic.  
- Displays scores, turn points, and active player using clean and formatted output.  

### 🧪 Testing the CLI

Run the CLI and test the following:

```bash
python -m pig_game
```

Then try these commands:

```
start
roll
hold
cheat
status
name TestPlayer
quit
```

**Expected behavior**:
- ✅ Friendly ⚠️ messages when game not started
- ✅ No crashes or errors
- ✅ Smooth user experience with clear feedback

---

## 🕹️ AI & HighScore Features

The Pig Game also supports playing against an AI opponent and viewing saved HighScores.

### ▶️ Start a Game vs CPU

```bash
python -m pig_game.shell ai --player "Mohammed" --level normal
```

#### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--player`, `-p` | Your displayed name | "Player" |
| `--level`, `-l` | CPU difficulty (`easy`, `normal`, `smart`) | `normal` |

#### Example Gameplay

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

At the end of the game, the system automatically records the result in the HighScore table (unless the player quits using `q`).

### 🏆 View HighScores

To view recorded results:

```bash
python -m pig_game.shell high --limit 10
```

#### Example output

```
Player         Vs     Result  For Against Duration(s)  When(UTC)
--------------------------------------------------------------------------------
Mohammed       CPU    win     150      64         250  2025-10-15T22:32:22Z
```

**Tip**: Use `--limit` to change how many rows are displayed.

### 💡 Notes

- The game's CPU uses `Intelligence.should_hold()` to decide whether to continue rolling or hold.
- High scores are stored locally at `~/.pig_highscores.json`.
- Invalid commands are handled safely (e.g., if the user types anything other than `r`, `h`, or `q`).

---

## 📊 UML Diagrams

We generate class and package diagrams using `pyreverse` (from `pylint`) and `Graphviz`.

### Prerequisites

Make sure you have:

1. **Graphviz** installed (verify with `dot -V`)
2. **pylint** and **graphviz** Python packages:

```bash
pip install pylint graphviz
```

Or install all dependencies at once:

```bash
make install
```

### Generate the Diagrams

To generate UML diagrams automatically, run:

```bash
make uml
```

This command will:
1. Run `pyreverse` on the `pig_game` package
2. Generate class and package diagrams
3. Save output files in the project directory

### Output Files

After running `make uml`, you should see:

- `classes_pig_game.png` — Class diagram showing all classes and their relationships
- `packages_pig_game.png` — Package diagram showing module structure

### View the Diagrams

Open the generated PNG files:

```bash
# On Linux
xdg-open classes_pig_game.png

# On macOS
open classes_pig_game.png

# On Windows
start classes_pig_game.png
```

### Verify UML Generation

To verify the UML generation works correctly:

1. Run `make uml`
2. Check that `.png` files are created
3. Open and inspect the diagrams
4. Verify all classes and modules are included

---

## 📚 API Documentation

This project uses `pdoc` to generate API documentation for the `pig_game` package.

### Prerequisites

Make sure `pdoc` is installed:

```bash
python3 -m pip install pdoc
```

Or install all dependencies:

```bash
make install
```

### Generate Documentation

To regenerate the API documentation:

```bash
make doc
```

Or manually:

```bash
pdoc --html --output-dir docs pig_game
```

### View Documentation

After generation, open the documentation:

```bash
# The documentation will be in the docs/ directory
open docs/pig_game/index.html
```

Or serve it locally:

```bash
pdoc --http : pig_game
```

Then visit `http://localhost:8080/pig_game` in your browser.

### What's Documented

The API documentation includes:
- All public classes and methods
- Function signatures and parameters
- Docstrings from the code
- Module-level documentation
- Inheritance hierarchies

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

Run and test the CLI:

```bash
python -m pig_game
```

Expected behavior:
- ✅ Friendly messages when game not started
- ✅ No crashes or errors
- ✅ Smooth user experience with clear feedback

---

## 👨‍💻 Contributors

**Mohammed Nour** — CLI implementation, AI & HighScore integration, error handling, and documentation.

---

## 📄 License

This project is licensed under the terms described in `LICENSE.md`.

---

## 🚀 Quick Start Guide

```bash
# 1. Install dependencies
make install

# 2. Play the game
python -m pig_game

# 3. Play against AI
python -m pig_game.shell ai --player "YourName" --level normal

# 4. View high scores
python -m pig_game.shell high

# 5. Generate UML diagrams
make uml

# 6. Generate API docs
make doc
```

---

**Happy Gaming! 🎲✨**


## 🎬 Video Demonstration

[**Watch Project Video Presentation**](https://youtu.be/n_nbSjPXyz4)

**Video includes:**
- Introduction and project overview
- Game demonstration (CLI gameplay)
- AI opponent demonstration
- Comprehensive testing (87% coverage)
- API documentation and UML diagrams
- Code quality walkthrough

**Duration:** 9-10 minutes