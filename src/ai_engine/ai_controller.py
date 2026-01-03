"""
AI Controller - TV1 & TV3 (Trí Hoằng & Trọng Đức)
Controller thông minh với difficulty-based behavior

Tích hợp:
- Neural Network decisions
- Ball prediction algorithms  
- Difficulty modifiers
- Reaction time simulation
"""
import neat
from .predictor import BallPredictor
from .difficulty_system import AIBehaviorModifier


class AIController:
    """
    Advanced AI controller với difficulty-based behavior
    Kết hợp NEAT neural network + physics prediction + behavior modifiers
    """
    
    def __init__(self, neural_net, config, difficulty='medium', 
                 window_width=800, window_height=600, 
                 paddle_width=20, paddle_height=100):
        """
        Initialize AI controller
        
        Args:
            neural_net: NEAT neural network
            config: NEAT config
            difficulty: 'easy', 'medium', or 'hard'
            window_width: Window width
            window_height: Window height
            paddle_width: Paddle width
            paddle_height: Paddle height
        """
        self.net = neural_net
        self.config = config
        self.difficulty = difficulty
        
        # Initialize behavior modifier
        self.behavior = AIBehaviorModifier(difficulty)
        
        # Initialize predictor
        self.predictor = BallPredictor(
            window_width, window_height,
            paddle_width, paddle_height
        )
        
        self.window_width = window_width
        self.window_height = window_height
        self.paddle_height = paddle_height
        
    def get_action(self, ball_x, ball_y, ball_vx, ball_vy, 
                   paddle_x, paddle_y, ball_radius=7):
        """
        Get AI action với difficulty-based behavior
        
        Args:
            ball_x, ball_y: Ball position
            ball_vx, ball_vy: Ball velocity
            paddle_x, paddle_y: Paddle position
            ball_radius: Ball radius
            
        Returns:
            int: Action (0=stay, 1=up, 2=down)
        """
        # Check if AI should react (EASY mode may not react if ball is far)
        if not self.behavior.should_react(ball_x, ball_vx, paddle_x, self.window_width):
            return 0  # Stay
        
        # Apply reaction delay
        if not self.behavior.apply_reaction_delay():
            return self.behavior.last_decision  # Use previous decision
        
        # Determine if paddle is on right or left
        is_right_paddle = paddle_x > self.window_width / 2
        
        # Get target position using prediction
        if self.behavior.should_use_advanced_prediction():
            # Use advanced ball prediction
            target_y = self.predictor.get_intercept_point(
                ball_x, ball_y, ball_vx, ball_vy,
                ball_radius, paddle_x, not is_right_paddle
            )
            
            # Apply prediction accuracy modifier
            target_y = self.behavior.apply_prediction_accuracy(
                target_y, ball_y, self.window_height
            )
        else:
            # Simple prediction: just follow ball Y (EASY mode)
            target_y = ball_y
            
            # Add some random offset for easy mode
            if self.difficulty == 'easy':
                import random
                offset = random.uniform(-50, 50)
                target_y += offset
        
        # Get neural network input
        inputs = self._get_neural_inputs(
            ball_x, ball_y, ball_vx, ball_vy, paddle_y, target_y
        )
        
        # Get raw neural network output
        output = self.net.activate(inputs)
        
        # Process output with behavior modifiers
        decision = self.behavior.process_neural_output(
            output[0], paddle_y, target_y, self.paddle_height
        )
        
        # Store decision for delay system
        self.behavior.last_decision = decision
        
        return decision
    
    def _get_neural_inputs(self, ball_x, ball_y, ball_vx, ball_vy, 
                          paddle_y, target_y):
        """
        Chuẩn bị inputs cho neural network
        
        Args:
            ball_x, ball_y: Ball position
            ball_vx, ball_vy: Ball velocity  
            paddle_y: Paddle Y position
            target_y: Target Y position
            
        Returns:
            tuple: Normalized inputs
        """
        # Normalize inputs to [0, 1] or [-1, 1]
        norm_ball_x = ball_x / self.window_width
        norm_ball_y = ball_y / self.window_height
        norm_ball_vx = ball_vx / 10  # Typical max velocity ~10
        norm_ball_vy = ball_vy / 10
        norm_paddle_y = paddle_y / self.window_height
        
        return (norm_ball_x, norm_ball_y, norm_ball_vx, norm_ball_vy, norm_paddle_y)
    
    def get_move_direction(self, action, paddle_y):
        """
        Convert action to move direction
        
        Args:
            action: AI action (0=stay, 1=up, 2=down)
            paddle_y: Current paddle Y
            
        Returns:
            int: -1 (up), 0 (stay), 1 (down)
        """
        if action == 1:
            return -1  # Up
        elif action == 2:
            return 1  # Down
        else:
            return 0  # Stay
    
    def get_speed_factor(self):
        """
        Get paddle speed multiplier based on difficulty
        
        Returns:
            float: Speed factor (0.0 to 1.0)
        """
        return self.behavior.get_speed_factor()


def create_ai_controller(genome, config, difficulty, window_width=800, window_height=600):
    """
    Factory function to create AI controller
    
    Args:
        genome: NEAT genome
        config: NEAT config
        difficulty: 'easy', 'medium', or 'hard'
        window_width: Window width
        window_height: Window height
        
    Returns:
        AIController: Configured AI controller
    """
    # Create neural network
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    
    # Create controller
    controller = AIController(
        net, config, difficulty,
        window_width, window_height
    )
    
    return controller
