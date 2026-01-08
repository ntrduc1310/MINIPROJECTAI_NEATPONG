"""
Unit Tests for Ball Class
Testing ball physics, movement, and modifiers.

Run tests:
    pytest tests/test_ball.py -v
    pytest tests/test_ball.py::TestBall::test_initialization -v
"""
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from game_engine.ball import Ball


class TestBallInitialization:
    """Test ball initialization and validation."""
    
    def test_valid_initialization(self):
        """Test ball creation with valid parameters."""
        ball = Ball(400, 300)
        assert ball.x == 400
        assert ball.y == 300
        assert ball.original_x == 400
        assert ball.original_y == 300
        assert ball.speed_modifier == 1.0
    
    def test_initialization_converts_to_float(self):
        """Test that coordinates are converted to float."""
        ball = Ball(100, 200)
        assert isinstance(ball.x, float)
        assert isinstance(ball.y, float)
    
    def test_negative_coordinates_raise_error(self):
        """Test that negative coordinates raise ValueError."""
        with pytest.raises(ValueError, match="must be non-negative"):
            Ball(-10, 300)
        
        with pytest.raises(ValueError, match="must be non-negative"):
            Ball(400, -20)
    
    def test_non_numeric_coordinates_raise_error(self):
        """Test that non-numeric coordinates raise TypeError."""
        with pytest.raises(TypeError, match="must be numeric"):
            Ball("400", 300)
        
        with pytest.raises(TypeError, match="must be numeric"):
            Ball(400, None)
    
    def test_velocity_initialization(self):
        """Test that velocities are initialized correctly."""
        ball = Ball(400, 300)
        
        # Velocity should be non-zero
        assert ball.x_vel != 0
        assert ball.y_vel != 0
        
        # Should not exceed MAX_VEL
        assert abs(ball.x_vel) <= Ball.MAX_VEL
        assert abs(ball.y_vel) <= Ball.MAX_VEL


class TestBallMovement:
    """Test ball movement mechanics."""
    
    def test_move_updates_position(self):
        """Test that move() updates ball position."""
        ball = Ball(400, 300)
        initial_x = ball.x
        initial_y = ball.y
        
        ball.move()
        
        # Position should change (unless velocity is exactly 0, which shouldn't happen)
        assert ball.x != initial_x or ball.y != initial_y
    
    def test_move_respects_speed_modifier(self):
        """Test that speed modifier affects movement."""
        ball1 = Ball(400, 300)
        ball2 = Ball(400, 300)
        
        # Set same velocity
        ball1.x_vel = 5.0
        ball1.y_vel = 3.0
        ball2.x_vel = 5.0
        ball2.y_vel = 3.0
        
        # Set different modifiers
        ball1.speed_modifier = 1.0
        ball2.speed_modifier = 2.0
        
        ball1.move()
        ball2.move()
        
        # Ball2 should move twice as far
        assert abs(ball2.x - 400) == pytest.approx(2 * abs(ball1.x - 400))
        assert abs(ball2.y - 300) == pytest.approx(2 * abs(ball1.y - 300))


class TestBallReset:
    """Test ball reset functionality."""
    
    def test_reset_position(self):
        """Test that reset() restores original position."""
        ball = Ball(400, 300)
        
        # Move ball
        ball.x = 500
        ball.y = 400
        
        ball.reset()
        
        assert ball.x == 400
        assert ball.y == 300
    
    def test_reset_velocity(self):
        """Test that reset() generates new velocity."""
        ball = Ball(400, 300)
        
        old_x_vel = ball.x_vel
        old_y_vel = ball.y_vel
        
        ball.reset()
        
        # Velocity should change (random)
        # Note: There's a tiny chance this could fail if random happens to generate same values
        assert ball.x_vel != old_x_vel or ball.y_vel != old_y_vel
    
    def test_reset_reverses_x_direction(self):
        """Test that reset() reverses X direction."""
        ball = Ball(400, 300)
        
        original_x_vel_sign = 1 if ball.x_vel > 0 else -1
        ball.reset()
        new_x_vel_sign = 1 if ball.x_vel > 0 else -1
        
        # Direction should be opposite
        assert original_x_vel_sign != new_x_vel_sign
    
    def test_reset_speed_modifier(self):
        """Test that reset() resets speed modifier."""
        ball = Ball(400, 300)
        ball.speed_modifier = 2.0
        
        ball.reset()
        
        assert ball.speed_modifier == 1.0


class TestBallModifiers:
    """Test speed modifier functionality."""
    
    def test_apply_speed_modifier_valid(self):
        """Test applying valid speed modifiers."""
        ball = Ball(400, 300)
        
        ball.apply_speed_modifier(1.5)
        assert ball.speed_modifier == 1.5
        
        ball.apply_speed_modifier(0.5)
        assert ball.speed_modifier == 0.5
    
    def test_apply_speed_modifier_negative_raises_error(self):
        """Test that negative modifiers raise ValueError."""
        ball = Ball(400, 300)
        
        with pytest.raises(ValueError, match="must be positive"):
            ball.apply_speed_modifier(-1.0)
        
        with pytest.raises(ValueError, match="must be positive"):
            ball.apply_speed_modifier(0)
    
    def test_apply_speed_modifier_non_numeric_raises_error(self):
        """Test that non-numeric modifiers raise TypeError."""
        ball = Ball(400, 300)
        
        with pytest.raises(TypeError, match="must be numeric"):
            ball.apply_speed_modifier("1.5")
        
        with pytest.raises(TypeError, match="must be numeric"):
            ball.apply_speed_modifier(None)
    
    def test_extreme_speed_modifier_warning(self, capsys):
        """Test that extreme modifiers print warning."""
        ball = Ball(400, 300)
        
        ball.apply_speed_modifier(6.0)
        
        captured = capsys.readouterr()
        assert "[WARNING]" in captured.out
        assert "Extreme speed modifier" in captured.out


class TestBallConstants:
    """Test ball class constants."""
    
    def test_constants_are_correct_type(self):
        """Test that class constants have correct types."""
        assert isinstance(Ball.MAX_VEL, (int, float))
        assert isinstance(Ball.RADIUS, int)
    
    def test_constants_are_positive(self):
        """Test that constants are positive values."""
        assert Ball.MAX_VEL > 0
        assert Ball.RADIUS > 0


# Integration tests
class TestBallIntegration:
    """Integration tests for ball behavior."""
    
    def test_ball_bouncing_scenario(self):
        """Test a typical ball bouncing scenario."""
        ball = Ball(400, 300)
        
        # Simulate some movements
        for _ in range(10):
            ball.move()
        
        # Ball should have moved from initial position
        assert ball.x != 400 or ball.y != 300
    
    def test_multiple_resets(self):
        """Test multiple consecutive resets."""
        ball = Ball(400, 300)
        
        for _ in range(5):
            ball.move()
            ball.reset()
            assert ball.x == 400
            assert ball.y == 300
            assert ball.speed_modifier == 1.0


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
