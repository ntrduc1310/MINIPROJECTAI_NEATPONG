"""
Unit Tests for Paddle Class
Testing paddle physics, movement, and modifiers.

Run tests:
    pytest tests/test_paddle.py -v
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from game_engine.paddle import Paddle


class TestPaddleInitialization:
    """Test paddle initialization."""
    
    def test_valid_initialization(self):
        """Test paddle creation with valid parameters."""
        paddle = Paddle(10, 250)
        assert paddle.x == 10
        assert paddle.y == 250
        assert paddle.height_modifier == 1.0
        assert paddle.speed_modifier == 1.0
    
    def test_negative_coordinates_raise_error(self):
        """Test that negative coordinates raise ValueError."""
        with pytest.raises(ValueError):
            Paddle(-10, 250)


class TestPaddleMovement:
    """Test paddle movement."""
    
    def test_move_up(self):
        """Test moving paddle up."""
        paddle = Paddle(10, 250)
        initial_y = paddle.y
        
        paddle.move(up=True)
        
        assert paddle.y < initial_y
    
    def test_move_down(self):
        """Test moving paddle down."""
        paddle = Paddle(10, 250)
        initial_y = paddle.y
        
        paddle.move(up=False)
        
        assert paddle.y > initial_y


class TestPaddleModifiers:
    """Test paddle modifiers."""
    
    def test_apply_height_modifier(self):
        """Test height modifier application."""
        paddle = Paddle(10, 250)
        
        paddle.apply_height_modifier(1.5)
        assert paddle.height_modifier == 1.5
        assert paddle.get_current_height() == int(Paddle.HEIGHT * 1.5)
    
    def test_apply_speed_modifier(self):
        """Test speed modifier application."""
        paddle = Paddle(10, 250)
        
        paddle.apply_speed_modifier(2.0)
        assert paddle.speed_modifier == 2.0


class TestPaddleReset:
    """Test paddle reset."""
    
    def test_reset_position_and_modifiers(self):
        """Test that reset restores original state."""
        paddle = Paddle(10, 250)
        
        # Modify paddle
        paddle.x = 100
        paddle.y = 500
        paddle.apply_height_modifier(2.0)
        paddle.apply_speed_modifier(2.0)
        
        # Reset
        paddle.reset()
        
        assert paddle.x == 10
        assert paddle.y == 250
        assert paddle.height_modifier == 1.0
        assert paddle.speed_modifier == 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
