"""
AI Difficulty System - TV1 & TV3 (Trí Hoằng & Trọng Đức)
Hệ thống điều chỉnh độ khó AI với các thuật toán khác nhau

Chiến lược khác biệt hóa:
1. EASY: Reaction delay + random errors + simple prediction
2. MEDIUM: Balanced prediction + occasional mistakes
3. HARD: Perfect prediction + advanced strategies + no errors
"""
import random
import time


class DifficultyConfig:
    """Configuration cho từng difficulty level"""
    
    CONFIGS = {
        'easy': {
            # NEAT Training Parameters
            'generations': 30,
            'pop_size': 30,
            'fitness_threshold': 200,
            'min_species_size': 1,  # Allow single-member species
            
            # AI Behavior Parameters
            'reaction_delay': 0.15,  # 150ms delay (human-like)
            'prediction_accuracy': 0.6,  # 60% accurate predictions
            'error_rate': 0.25,  # 25% chance of wrong decision
            'look_ahead_steps': 3,  # Short prediction
            'decision_threshold': 0.3,  # Less decisive (0.3 instead of 0.5)
            'use_advanced_prediction': False,
            'max_speed_factor': 0.7,  # 70% of max paddle speed
            
            # Strategy
            'strategy': 'reactive',  # Chỉ react khi bóng gần
            'activation_distance': 300,  # Chỉ di chuyển khi bóng < 300px
        },
        
        'medium': {
            # NEAT Training Parameters
            'generations': 60,
            'pop_size': 50,
            'fitness_threshold': 350,
            'min_species_size': 1,
            
            # AI Behavior Parameters
            'reaction_delay': 0.05,  # 50ms delay
            'prediction_accuracy': 0.85,  # 85% accurate
            'error_rate': 0.10,  # 10% mistakes
            'look_ahead_steps': 8,  # Medium prediction
            'decision_threshold': 0.5,  # Normal decisiveness
            'use_advanced_prediction': True,
            'max_speed_factor': 0.9,  # 90% speed
            
            # Strategy
            'strategy': 'predictive',  # Predict trajectory
            'activation_distance': 600,  # React earlier
        },
        
        'hard': {
            # NEAT Training Parameters
            'generations': 100,
            'pop_size': 200,  # Tăng lên 200 để tránh conflict với species
            'fitness_threshold': 500,
            'min_species_size': 1,
            
            # AI Behavior Parameters
            'reaction_delay': 0.0,  # No delay (perfect reflexes)
            'prediction_accuracy': 1.0,  # 100% accurate
            'error_rate': 0.0,  # No errors
            'look_ahead_steps': 15,  # Long-term prediction
            'decision_threshold': 0.7,  # Very decisive
            'use_advanced_prediction': True,
            'max_speed_factor': 1.0,  # Full speed
            
            # Strategy
            'strategy': 'optimal',  # Perfect positioning
            'activation_distance': 800,  # Always active
        }
    }
    
    @classmethod
    def get_config(cls, difficulty):
        """
        Lấy config cho difficulty level
        
        Args:
            difficulty: 'easy', 'medium', or 'hard'
            
        Returns:
            dict: Configuration parameters
        """
        if difficulty not in cls.CONFIGS:
            raise ValueError(f"Invalid difficulty: {difficulty}")
        return cls.CONFIGS[difficulty].copy()


class AIBehaviorModifier:
    """
    Modify AI behavior based on difficulty
    Áp dụng các thuật toán để tạo sự khác biệt
    """
    
    def __init__(self, difficulty='medium'):
        """
        Initialize behavior modifier
        
        Args:
            difficulty: 'easy', 'medium', or 'hard'
        """
        self.difficulty = difficulty
        self.config = DifficultyConfig.get_config(difficulty)
        self.last_decision_time = 0
        self.last_decision = 0
        
    def should_react(self, ball_x, ball_vx, paddle_x, window_width):
        """
        Xác định AI có nên react không (EASY mode: chỉ react khi bóng gần)
        
        Args:
            ball_x: Ball X position
            ball_vx: Ball X velocity
            paddle_x: Paddle X position
            window_width: Window width
            
        Returns:
            bool: True if AI should react
        """
        # HARD/MEDIUM: Always react
        if self.difficulty in ['hard', 'medium']:
            return True
        
        # EASY: Only react when ball is close
        distance = abs(ball_x - paddle_x)
        activation_distance = self.config['activation_distance']
        
        # Check if ball is moving towards paddle
        is_right_paddle = paddle_x > window_width / 2
        ball_moving_towards = (is_right_paddle and ball_vx > 0) or (not is_right_paddle and ball_vx < 0)
        
        return ball_moving_towards and distance < activation_distance
    
    def apply_reaction_delay(self):
        """
        Áp dụng reaction delay (human-like behavior)
        
        Returns:
            bool: True if enough time has passed since last decision
        """
        current_time = time.time()
        delay = self.config['reaction_delay']
        
        if current_time - self.last_decision_time >= delay:
            self.last_decision_time = current_time
            return True
        return False
    
    def apply_decision_error(self, optimal_decision):
        """
        Áp dụng error rate vào decision (simulate mistakes)
        
        Args:
            optimal_decision: The optimal decision (0=stay, 1=up, 2=down)
            
        Returns:
            int: Modified decision
        """
        error_rate = self.config['error_rate']
        
        if random.random() < error_rate:
            # Make a mistake
            possible_decisions = [0, 1, 2]
            possible_decisions.remove(optimal_decision)
            return random.choice(possible_decisions)
        
        return optimal_decision
    
    def apply_prediction_accuracy(self, prediction_y, ball_y, window_height):
        """
        Giảm độ chính xác của prediction (add noise)
        
        Args:
            prediction_y: Predicted Y position
            ball_y: Current ball Y
            window_height: Window height
            
        Returns:
            float: Modified prediction with noise
        """
        accuracy = self.config['prediction_accuracy']
        
        if accuracy >= 1.0:
            return prediction_y  # Perfect prediction
        
        # Add gaussian noise proportional to (1 - accuracy)
        max_error = window_height * 0.2  # Max 20% of screen
        noise_std = max_error * (1 - accuracy)
        noise = random.gauss(0, noise_std)
        
        # Blend between prediction and current position based on accuracy
        noisy_prediction = prediction_y + noise
        
        # Clamp to valid range
        return max(0, min(window_height, noisy_prediction))
    
    def get_decision_threshold(self):
        """
        Lấy threshold cho decision making
        
        Returns:
            float: Decision threshold
        """
        return self.config['decision_threshold']
    
    def get_speed_factor(self):
        """
        Lấy speed factor cho paddle movement
        
        Returns:
            float: Speed multiplier (0.0 to 1.0)
        """
        return self.config['max_speed_factor']
    
    def should_use_advanced_prediction(self):
        """
        Check if should use advanced ball prediction
        
        Returns:
            bool: True if advanced prediction should be used
        """
        return self.config['use_advanced_prediction']
    
    def get_look_ahead_steps(self):
        """
        Số bước prediction cho AI
        
        Returns:
            int: Number of simulation steps
        """
        return self.config['look_ahead_steps']
    
    def process_neural_output(self, output, paddle_y, target_y, paddle_height):
        """
        Xử lý output từ neural network với difficulty modifiers
        
        Args:
            output: Raw neural network output
            paddle_y: Current paddle Y position
            target_y: Target Y position
            paddle_height: Paddle height
            
        Returns:
            int: Final decision (0=stay, 1=up, 2=down)
        """
        threshold = self.get_decision_threshold()
        paddle_center = paddle_y + paddle_height / 2
        
        # Determine optimal decision
        if abs(target_y - paddle_center) < 10:
            optimal = 0  # Stay
        elif target_y < paddle_center:
            optimal = 1  # Up
        else:
            optimal = 2  # Down
        
        # Apply error rate
        decision = self.apply_decision_error(optimal)
        
        return decision


def get_neat_config_for_difficulty(difficulty, base_config_path):
    """
    Tạo NEAT config tùy chỉnh cho difficulty level
    
    Args:
        difficulty: 'easy', 'medium', or 'hard'
        base_config_path: Path to base config file
        
    Returns:
        dict: Modified NEAT parameters
    """
    import neat
    
    # Load base config
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        base_config_path
    )
    
    # Get difficulty config
    diff_config = DifficultyConfig.get_config(difficulty)
    
    # Modify parameters based on difficulty
    config.pop_size = diff_config['pop_size']
    config.fitness_threshold = diff_config['fitness_threshold']
    
    # Adjust genome parameters for different complexities
    if difficulty == 'easy':
        # Simpler networks
        config.genome_config.num_hidden = 0  # No hidden layers
        config.genome_config.conn_add_prob = 0.2
        config.genome_config.node_add_prob = 0.1
    elif difficulty == 'medium':
        # Medium complexity
        config.genome_config.num_hidden = 2
        config.genome_config.conn_add_prob = 0.4
        config.genome_config.node_add_prob = 0.2
    else:  # hard
        # Complex networks
        config.genome_config.num_hidden = 4
        config.genome_config.conn_add_prob = 0.6
        config.genome_config.node_add_prob = 0.3
    
    return config
