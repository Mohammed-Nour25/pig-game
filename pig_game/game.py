"""Game core (M1-2: Game actions + cheat placeholder).

Manages:
- players list (two players by default)
- per-player scores
- current turn total
- active player index
- goal score

Implements:
- roll(): add dice value; if 1 → bust (reset turn) and switch turn
- hold(): bank turn_total to active player; reset; switch unless already winner
- switch_turn(): toggle active player index
- is_winner(): check if a player reached goal
- cheat(): add +90 points to the active player (placeholder)
"""

from __future__ import annotations
from typing import List, Optional
import random


class Game:
    """Core Pig game logic."""

    def __init__(self, goal: int = 100, players: Optional[List[str]] = None) -> None:
        """
        Initialize a new game state.

        Args:
            goal: Target score to win (must be > 0).
            players: Optional list of two player names.
                     Defaults to ["Player 1", "Player 2"].
        """
        if goal <= 0:
            raise ValueError("goal must be positive")

        self.goal: int = goal

        # Initialize players
        if players is None:
            players = ["Player 1", "Player 2"]
        if len(players) != 2:
            raise ValueError("Pig requires exactly two players")

        self.players: List[str] = players

        # Initialize scores for each player
        self.scores: List[int] = [0, 0]

        # Track current turn total and active player
        self.turn_total: int = 0
        self.active_index: int = 0  # 0 = Player 1, 1 = Player 2

    # --- Convenience properties ---
    @property
    def active(self) -> str:
        """Return the active player's name."""
        return self.players[self.active_index]

    @property
    def waiting(self) -> str:
        """Return the non-active player's name."""
        return self.players[1 - self.active_index]

    # --- Core actions ---
    def roll(self) -> int:
        """
        Roll a six-sided die and update the turn state.

        Returns:
            The rolled value in [1, 6].

        Rules:
            - If value == 1: bust → reset turn_total and switch turn.
            - Else: add value to turn_total and keep the same player.
        """
        value = random.randint(1, 6)
        if value == 1:
            self.turn_total = 0
            self.switch_turn()
        else:
            self.turn_total += value
        return value

    def hold(self) -> None:
        """
        Bank the current turn_total into the active player's score.

        After holding:
            - turn_total resets to 0.
            - If the active player has not yet won, switch the turn.
            - If the active player reached the goal, keep the turn (game won).
        """
        self.scores[self.active_index] += self.turn_total
        self.turn_total = 0

        if not self.is_winner(self.active_index):
            self.switch_turn()

    def switch_turn(self) -> None:
        """Toggle the active player index (0 ↔ 1)."""
        self.active_index = 1 - self.active_index

    def is_winner(self, player_index: Optional[int] = None) -> bool:
        """
        Check whether a player has reached the goal score.

        Args:
            player_index: Index of the player to check; defaults to the active player.

        Returns:
            True if the player's score >= goal, else False.
        """
        idx = self.active_index if player_index is None else player_index
        return self.scores[idx] >= self.goal

    def cheat(self) -> None:
        """
        Add +90 points to the active player's score (for testing or fun).

        This is a placeholder cheat method as part of M1-2.
        """
        self.scores[self.active_index] += 90
