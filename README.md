# 🎲 Pig (Dice Game) — TDD Project

> **Note:** This repository is a **skeleton** project — it contains no full implementation yet.  
> The goal is to enable team members to implement features (M1 / M2 / M3) in separate branches and pull requests following the **Test-Driven Development (TDD)** approach.

---

## 🎯 Project Overview
The **Pig Dice Game** is a simple turn-based dice game implemented in **Python**.  
This project follows the **Test-Driven Development (TDD)** methodology — all features should be implemented by writing tests first, then adding the code that makes those tests pass.

---

## 🚀 Getting Started

1. **Create your feature branch**
   ```bash
   git checkout -b feat/m1-game-core-yourname
   ```

2. **Write tests first**, then implement the necessary code until all tests pass ✅  
3. Open a **Pull Request** and request a review.

---

## 🧰 Available Commands

```bash
python -m pip install -r requirements.txt
make test        # run tests (currently placeholders)
make lint        # run code linters (flake8 + pylint)
make doc         # generate API documentation in doc/api/
make uml         # generate UML diagrams in doc/uml/
```

---

## 🧩 Milestone Breakdown (Editable)

### M1 - Core Game & CLI
- Classes: `Game`, `Dice`, `Player` (optional: `DiceHand`)
- Command-line interface via `PigShell(cmd.Cmd)`
  - Commands: `start`, `roll`, `hold`, `status`, `name`, `rules`, `cheat`, `quit`
- Support for two players + CPU mode (optional)
- Unit tests with ≥90% coverage

### M2 - Highscore & AI
- AI intelligence levels (easy / medium / hard)
- Highscore management in JSON format
- New CLI commands: `ai`, `high`
- Integration with end-of-game events

### M3 - Documentation, UML, Linters, Coverage
- ≥90% test coverage
- Full code linting: flake8 / pylint / black
- Generate documentation with `pdoc` and UML with `pyreverse`
- Update README and presentation video

---

## 🏗️ Project Structure

```
pig_game/
  dice.py
  player.py
  game.py
  intelligence.py
  highscore.py
  shell.py
  __main__.py        # CLI entry point
tests/
  test_*.py          # placeholder unit tests
doc/api/             # generated documentation
doc/uml/             # UML diagrams
```

---

## ▶️ How to Run

After implementing the core game logic (M1):

```bash
python -m pig_game
```

---

## 🎮 Command-Line Interface (CLI)

You can play the Pig game directly from the terminal using the built-in CLI.

### How to run
```bash
python -m pig_game
```

### Available commands
- `rules` → show game rules  
- `start [goal]` → start a new game (default = 100)  
- `status` → show current player and scores  
- `roll` → roll the die for the current player  
- `hold` → bank points and switch turn  
- `name <new_name>` → change the active player's name  
- `cheat` → add +90 points (for testing)  
- `quit` → exit the game  

### Example session
```
$ python -m pig_game
Welcome to Pig! Type 'help' or '?' for commands.

(pig) rules
Pig — Rules:
- Players take turns rolling one die.
- Add roll to turn points...
(pig) start
New game started. Goal = 100.
(pig) roll
Rolled: 4
(pig) hold
Points banked. Turn passed to next player.
(pig) quit
Bye!
```

---

## 📜 License
This project is licensed under the [MIT License](LICENSE.md).

---

## 🌟 Contributors
This repository is part of a **collaborative training project** focused on mastering **Test-Driven Development (TDD)** with Python.  
Contributions and improvements are always welcome!

---

## 📸 (Optional Later)
> You can add screenshots or GIFs of the CLI once the game logic and interface are implemented.

---

![CI](https://github.com/Mohammed-Nour25/pig-game/actions/workflows/ci.yml/badge.svg)
