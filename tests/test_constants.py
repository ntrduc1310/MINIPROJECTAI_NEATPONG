"""
Unit Tests for Constants Module
Testing configuration constants validation.

Run tests:
    pytest tests/test_constants.py -v
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.constants import (
    GameConstants, 
    TrainingConstants, 
    UIConstants,
    PowerUpConstants,
    validate_constants
)


class TestGameConstants:
    """Test game configuration constants."""
    
    def test_window_dimensions_positive(self):
        """Test that window dimensions are positive."""
        assert GameConstants.WINDOW_WIDTH > 0
        assert GameConstants.WINDOW_HEIGHT > 0
    
    def test_paddle_fits_in_window(self):
        """Test that paddle fits within window height."""
        assert GameConstants.PADDLE_HEIGHT <= GameConstants.WINDOW_HEIGHT
    
    def test_spawn_positions(self):
        """Test spawn position calculations."""
        left_x, left_y = GameConstants.get_paddle_spawn_left()
        right_x, right_y = GameConstants.get_paddle_spawn_right()
        ball_x, ball_y = GameConstants.get_ball_spawn()
        
        # Check positions are within bounds
        assert 0 <= left_x < GameConstants.WINDOW_WIDTH
        assert 0 <= right_x < GameConstants.WINDOW_WIDTH
        assert 0 <= ball_x < GameConstants.WINDOW_WIDTH
        
        assert 0 <= left_y < GameConstants.WINDOW_HEIGHT
        assert 0 <= right_y < GameConstants.WINDOW_HEIGHT
        assert 0 <= ball_y < GameConstants.WINDOW_HEIGHT


class TestTrainingConstants:
    """Test training configuration constants."""
    
    def test_difficulty_configs_exist(self):
        """Test that all difficulty configs are defined."""
        assert 'easy' in TrainingConstants.DIFFICULTY_CONFIGS
        assert 'medium' in TrainingConstants.DIFFICULTY_CONFIGS
        assert 'hard' in TrainingConstants.DIFFICULTY_CONFIGS
    
    def test_get_difficulty_config_valid(self):
        """Test getting valid difficulty configs."""
        easy_config = TrainingConstants.get_difficulty_config('easy')
        assert 'generations' in easy_config
        assert 'pop_size' in easy_config
        assert easy_config['generations'] > 0
    
    def test_get_difficulty_config_invalid(self):
        """Test that invalid difficulty raises error."""
        with pytest.raises(ValueError, match="Invalid difficulty"):
            TrainingConstants.get_difficulty_config('impossible')
    
    def test_neural_network_structure(self):
        """Test neural network input/output structure."""
        assert TrainingConstants.NUM_INPUTS > 0
        assert TrainingConstants.NUM_OUTPUTS > 0


class TestUIConstants:
    """Test UI configuration constants."""
    
    def test_colors_are_valid_rgb(self):
        """Test that color tuples are valid RGB."""
        colors_to_test = [
            UIConstants.COLOR_BLACK,
            UIConstants.COLOR_WHITE,
            UIConstants.COLOR_RED,
            UIConstants.COLOR_PADDLE,
            UIConstants.COLOR_BALL
        ]
        
        for color in colors_to_test:
            assert len(color) == 3, f"Color {color} must have 3 values"
            assert all(0 <= c <= 255 for c in color), f"Color {color} values must be 0-255"
    
    def test_font_sizes_positive(self):
        """Test that font sizes are positive."""
        assert UIConstants.FONT_SIZE_TITLE > 0
        assert UIConstants.FONT_SIZE_LARGE > 0
        assert UIConstants.FONT_SIZE_MEDIUM > 0


class TestPowerUpConstants:
    """Test power-up configuration constants."""
    
    def test_power_up_types_defined(self):
        """Test that power-up types are defined."""
        assert len(PowerUpConstants.POWER_UP_TYPES) > 0
        
        for power_type, config in PowerUpConstants.POWER_UP_TYPES.items():
            assert 'color' in config
            assert 'effect' in config
            assert 'modifier' in config
    
    def test_probabilities_sum_to_one(self):
        """Test that power-up probabilities sum to 1.0."""
        total = sum(PowerUpConstants.POWER_UP_PROBABILITIES.values())
        assert abs(total - 1.0) < 0.01, f"Probabilities sum to {total}, expected 1.0"
    
    def test_spawn_settings_positive(self):
        """Test that spawn settings are positive."""
        assert PowerUpConstants.SPAWN_INTERVAL > 0
        assert PowerUpConstants.LIFETIME > 0


class TestConstantsValidation:
    """Test constants validation function."""
    
    def test_validation_passes(self):
        """Test that validation passes for current constants."""
        # Should not raise any errors
        assert validate_constants() == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
