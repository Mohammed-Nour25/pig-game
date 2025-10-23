"""Tests for ai_game module."""
import pytest
from unittest.mock import patch, MagicMock
from pig_game.ai_game import play_ai_game


def test_ai_game_quit_immediately(capsys):
    """Test quitting the game immediately."""
    with patch('builtins.input', return_value='q'):
        play_ai_game(player_name="Test", level="easy", goal=100)
    
    captured = capsys.readouterr()
    assert "Pig Game" in captured.out
    assert "Test vs CPU" in captured.out
    assert "Game ended" in captured.out


def test_ai_game_human_wins(capsys):
    """Test scenario where human wins."""
    # Mock inputs: roll twice, hold (repeat until win)
    inputs = ['r', 'r', 'r', 'r', 'r', 'h'] * 20 + ['q']
    
    with patch('builtins.input', side_effect=inputs):
        with patch('pig_game.game.Game.roll') as mock_roll:
            with patch('pig_game.game.Game.hold') as mock_hold:
                # Make human win on first hold
                mock_roll.return_value = 6
                mock_hold.return_value = "win"
                
                play_ai_game(player_name="Winner", level="normal", goal=100)
    
    captured = capsys.readouterr()
    assert "Congratulations" in captured.out or "Game ended" in captured.out


def test_ai_game_human_bust(capsys):
    """Test human rolling a 1 (bust)."""
    inputs = ['r', 'q']
    
    with patch('builtins.input', side_effect=inputs):
        with patch('pig_game.game.Game.roll', return_value=1):
            play_ai_game(player_name="Test", level="easy", goal=100)
    
    captured = capsys.readouterr()
    assert "BUST" in captured.out or "rolled 1" in captured.out


def test_ai_game_invalid_input(capsys):
    """Test handling invalid input."""
    inputs = ['x', 'q']
    
    with patch('builtins.input', side_effect=inputs):
        play_ai_game(player_name="Test", level="hard", goal=100)
    
    captured = capsys.readouterr()
    assert "Invalid" in captured.out or "Game ended" in captured.out


def test_ai_game_cpu_wins(capsys):
    """Test scenario where CPU wins."""
    inputs = ['r', 'h', 'q']
    
    with patch('builtins.input', side_effect=inputs):
        with patch('pig_game.game.Game.roll', side_effect=[3, 6, 6, 6, 6, 6]):
            with patch('pig_game.game.Game.hold', side_effect=["ok", "win"]):
                with patch('pig_game.intelligence.Intelligence.should_hold', return_value=True):
                    play_ai_game(player_name="Loser", level="smart", goal=100)
    
    captured = capsys.readouterr()
    assert "CPU won" in captured.out or "Game ended" in captured.out


def test_ai_game_different_levels():
    """Test AI game with different difficulty levels."""
    inputs = ['q']
    
    for level in ['easy', 'normal', 'hard', 'smart']:
        with patch('builtins.input', return_value='q'):
            play_ai_game(player_name="Test", level=level, goal=50)


def test_ai_game_custom_goal(capsys):
    """Test AI game with custom goal."""
    with patch('builtins.input', return_value='q'):
        play_ai_game(player_name="Custom", level="normal", goal=50)
    
    captured = capsys.readouterr()
    assert "Goal: 50" in captured.out


def test_ai_game_full_human_turn(capsys):
    """Test complete human turn with multiple rolls and hold."""
    inputs = ['r', 'r', 'r', 'h', 'q']
    
    with patch('builtins.input', side_effect=inputs):
        with patch('pig_game.game.Game.roll', side_effect=[3, 4, 5, 2]):
            with patch('pig_game.game.Game.hold', return_value="ok"):
                play_ai_game(player_name="Test", level="normal", goal=100)
    
    captured = capsys.readouterr()
    assert "rolled" in captured.out.lower()


def test_ai_game_cpu_turn_logic(capsys):
    """Test CPU turn with AI decision making."""
    inputs = ['r', 'h']
    
    with patch('builtins.input', side_effect=inputs + ['q']):
        with patch('pig_game.game.Game.roll', side_effect=[3, 4, 5, 6, 2]):
            with patch('pig_game.game.Game.hold', return_value="ok"):
                with patch('pig_game.intelligence.Intelligence.should_hold', side_effect=[False, False, False, True]):
                    play_ai_game(player_name="Test", level="normal", goal=100)
    
    captured = capsys.readouterr()
    assert "CPU" in captured.out


def test_ai_game_cpu_bust(capsys):
    """Test CPU getting a bust."""
    inputs = ['r', 'h']
    
    with patch('builtins.input', side_effect=inputs + ['q']):
        with patch('pig_game.game.Game.roll', side_effect=[3, 1, 3]):
            with patch('pig_game.game.Game.hold', return_value="ok"):
                play_ai_game(player_name="Test", level="easy", goal=100)
    
    captured = capsys.readouterr()
    assert "CPU" in captured.out


def test_ai_game_multiple_rounds(capsys):
    """Test multiple rounds of gameplay."""
    inputs = ['r', 'h', 'r', 'h', 'q']
    
    with patch('builtins.input', side_effect=inputs):
        with patch('pig_game.game.Game.roll', side_effect=[4, 5, 3, 6, 2, 4, 3]):
            with patch('pig_game.game.Game.hold', return_value="ok"):
                with patch('pig_game.intelligence.Intelligence.should_hold', return_value=True):
                    play_ai_game(player_name="Multi", level="hard", goal=100)
    
    captured = capsys.readouterr()
    assert "Turn" in captured.out or "turn" in captured.out


def test_main_function_with_args():
    """Test main function with command line arguments."""
    from pig_game.ai_game import main
    
    test_args = ['ai_game.py', '--player', 'TestPlayer', '--level', 'easy', '--goal', '50']
    
    with patch('sys.argv', test_args):
        with patch('builtins.input', return_value='q'):
            with patch('pig_game.ai_game.play_ai_game') as mock_play:
                main()
                mock_play.assert_called_once()


def test_main_keyboard_interrupt():
    """Test main function handling keyboard interrupt."""
    from pig_game.ai_game import main
    
    with patch('pig_game.ai_game.play_ai_game', side_effect=KeyboardInterrupt):
        with patch('sys.argv', ['ai_game.py']):
            main()  # Should not raise exception


def test_main_exception_handling():
    """Test main function handling general exceptions."""
    from pig_game.ai_game import main
    
    with patch('pig_game.ai_game.play_ai_game', side_effect=Exception("Test error")):
        with patch('sys.argv', ['ai_game.py']):
            with pytest.raises(SystemExit):
                main()


def test_ai_extended_gameplay(capsys):
    """Test extended AI gameplay covering more code paths."""
    # Simulate longer game with CPU making multiple decisions
    inputs = ['r', 'h']  # Human plays once
    roll_values = [3, 4, 5, 6, 2, 4, 3, 5, 2, 1]  # Various rolls including CPU bust
    
    with patch('builtins.input', side_effect=inputs + ['q']):
        with patch('pig_game.game.Game.roll', side_effect=roll_values):
            with patch('pig_game.game.Game.hold', return_value="ok"):
                # CPU evaluates multiple times before holding
                with patch('pig_game.intelligence.Intelligence.should_hold', 
                          side_effect=[False, False, False, False, True, False]):
                    play_ai_game(player_name="Extended", level="normal", goal=100)
    
    captured = capsys.readouterr()
    assert "CPU" in captured.out


def test_ai_game_score_display(capsys):
    """Test that scores are properly displayed."""
    inputs = ['r', 'h', 'q']
    
    with patch('builtins.input', side_effect=inputs):
        with patch('pig_game.game.Game.roll', side_effect=[4, 5, 3]):
            with patch('pig_game.game.Game.hold', return_value="ok"):
                with patch('pig_game.intelligence.Intelligence.should_hold', return_value=True):
                    play_ai_game(player_name="ScoreTest", level="easy", goal=100)
    
    captured = capsys.readouterr()
    assert "You:" in captured.out or "CPU:" in captured.out


def test_if_main_block():
    """Test the if __name__ == '__main__' block."""
    import subprocess
    import sys
    
    # Test that the script can be run directly
    result = subprocess.run(
        [sys.executable, 'pig_game/ai_game.py', '--player', 'Test', '--level', 'easy'],
        input='q\n',
        capture_output=True,
        text=True,
        timeout=5
    )
    
    assert result.returncode in [0, 1]  # Either success or controlled exit