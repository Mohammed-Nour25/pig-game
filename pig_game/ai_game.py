#!/usr/bin/env python3
"""
AI Gameplay mode for Pig Game.
Play against the computer with different difficulty levels.
"""

import sys
import argparse
from pig_game.game import Game
from pig_game.intelligence import Intelligence


def play_ai_game(player_name: str = "Player", level: str = "normal", goal: int = 100):
    """Play Pig game against AI opponent."""
    
    # Create game with player names as strings
    game = Game(players=[player_name, "CPU"], goal=goal)
    
    # Create AI
    ai = Intelligence(level=level)
    
    print(f"\n🎮 Pig Game - {player_name} vs CPU ({level} level)")
    print(f"🎯 Goal: {goal} points")
    print("=" * 50)
    
    # Game loop
    while True:
        is_human = (game.current == 0)  # Human is player 0
        human_score = game.scores[0]
        cpu_score = game.scores[1]
        turn_points = game.turn_total
        
        # Display scores
        print(f"\n{'Your' if is_human else 'CPU'} turn — "
              f"You: {human_score} | CPU: {cpu_score} | Turn: {turn_points}")
        
        if is_human:
            # Human turn
            while True:
                choice = input("[r=roll, h=hold, q=quit] > ").strip().lower()
                
                if choice == 'q':
                    print("👋 Game ended. Thanks for playing!")
                    return
                
                elif choice == 'r':
                    value = game.roll()
                    if value == 1:
                        print(f"🎲 You rolled 1. Turn points: 0 💥 BUST!")
                        break
                    else:
                        print(f"🎲 You rolled {value}. Turn points: {game.turn_total}")
                
                elif choice == 'h':
                    result = game.hold()
                    print(f"💾 You held. Your total is now {game.scores[0]}.")
                    if result == "win":
                        print(f"\n🏆 Congratulations! You won with {game.scores[0]} points! 🎉")
                        return
                    break
                
                else:
                    print("⚠️  Invalid input. Use 'r' (roll), 'h' (hold), or 'q' (quit).")
        
        else:
            # CPU turn
            print(f"\nCPU turn — CPU: {cpu_score} | You: {human_score} | Turn: {turn_points}")
            
            while True:
                # AI decides
                should_hold = ai.should_hold(
                    turn_points=game.turn_total,
                    total_score=game.scores[1],
                    opponent_score=game.scores[0],
                    goal=goal
                )
                
                if should_hold and game.turn_total > 0:
                    result = game.hold()
                    print(f"🤖 CPU holds. CPU total: {game.scores[1]}")
                    if result == "win":
                        print(f"\n💔 CPU won with {game.scores[1]} points. Better luck next time!")
                        return
                    break
                
                else:
                    value = game.roll()
                    if value == 1:
                        print(f"🤖 CPU rolled 1. CPU turn points: 0 💥 BUST!")
                        break
                    else:
                        print(f"🤖 CPU rolled {value}. CPU turn points: {game.turn_total}")


def main():
    """Parse arguments and start AI game."""
    parser = argparse.ArgumentParser(description="Play Pig against AI")
    parser.add_argument(
        "--player", "-p",
        default="Player",
        help="Your name (default: Player)"
    )
    parser.add_argument(
        "--level", "-l",
        default="normal",
        choices=["easy", "normal", "hard", "smart"],
        help="AI difficulty: easy, normal, hard/smart (default: normal)"
    )
    parser.add_argument(
        "--goal", "-g",
        type=int,
        default=100,
        help="Points needed to win (default: 100)"
    )
    
    args = parser.parse_args()
    
    try:
        play_ai_game(player_name=args.player, level=args.level, goal=args.goal)
    except KeyboardInterrupt:
        print("\n\n👋 Game interrupted. Bye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
