"""CLI Shell using cmd (skeleton).
TODO (M1 then M2):
- Create class PigShell(cmd.Cmd) with commands:
  start [goal], roll, hold, status, name <new_name>, rules, cheat, quit
- M2: add ai <level|number>, high
- Handle invalid input gracefully; integrate with Game/HighScore/Intelligence
- README: provide example CLI session
"""

from __future__ import annotations


class PigShell:  # pragma: no cover
    """cmd-based CLI (skeleton)."""

    def __init__(self) -> None:
        raise NotImplementedError("Implement PigShell for M1/M2")
