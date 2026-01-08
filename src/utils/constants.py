"""
Constants Module - Centralized configuration constants
Các hằng số cấu hình tập trung cho toàn bộ dự án.

Module này tập trung tất cả magic numbers và configuration values
vào một nơi để dễ quản lý và chỉnh sửa. Chia thành các categories:
- GameConstants: Game logic và physics
- TrainingConstants: NEAT training parameters  
- UIConstants: Colors, fonts, dimensions cho UI

Usage:
    >>> from utils.constants import GameConstants, UIConstants
    >>> window = pygame.display.set_mode((GameConstants.WINDOW_WIDTH, GameConstants.WINDOW_HEIGHT))
    >>> paddle = Paddle(speed=GameConstants.PADDLE_SPEED)
"""
from typing import Dict, Tuple
from enum import Enum


class Difficulty(Enum):
    """
    Enum cho các mức độ khó của AI.
    
    Sử dụng Enum thay vì string literals để tránh typos và
    có type safety tốt hơn.
    """
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class GameConstants:
    """
    Game logic và physics constants.
    
    Chứa tất cả constants liên quan đến game mechanics:
    - Window dimensions
    - Paddle properties
    - Ball properties
    - Physics parameters
    """
    
    # Window dimensions (pixels)
    WINDOW_WIDTH: int = 800
    WINDOW_HEIGHT: int = 600
    FPS: int = 60  # Frames per second
    
    # Paddle configuration
    PADDLE_WIDTH: int = 20
    PADDLE_HEIGHT: int = 100
    PADDLE_SPEED: float = 4.0  # Base speed (pixels per frame)
    PADDLE_OFFSET: int = 10    # Distance from screen edge
    
    # Ball configuration
    BALL_RADIUS: int = 7
    BALL_MAX_VELOCITY: float = 5.0  # Maximum speed (pixels per frame)
    BALL_INITIAL_ANGLE_MIN: int = -30  # Degrees
    BALL_INITIAL_ANGLE_MAX: int = 30   # Degrees
    
    # Scoring
    WINNING_SCORE: int = 10  # Points needed to win
    
    # Physics
    BALL_ACCELERATION: float = 1.1  # Multiplier on paddle hit
    MAX_BOUNCE_ANGLE: int = 45      # Maximum bounce angle (degrees)
    
    @classmethod
    def get_paddle_spawn_left(cls) -> Tuple[int, int]:
        """Vị trí spawn cho left paddle."""
        return (cls.PADDLE_OFFSET, cls.WINDOW_HEIGHT // 2 - cls.PADDLE_HEIGHT // 2)
    
    @classmethod
    def get_paddle_spawn_right(cls) -> Tuple[int, int]:
        """Vị trí spawn cho right paddle."""
        x = cls.WINDOW_WIDTH - cls.PADDLE_OFFSET - cls.PADDLE_WIDTH
        y = cls.WINDOW_HEIGHT // 2 - cls.PADDLE_HEIGHT // 2
        return (x, y)
    
    @classmethod
    def get_ball_spawn(cls) -> Tuple[int, int]:
        """Vị trí spawn cho ball (trung tâm màn hình)."""
        return (cls.WINDOW_WIDTH // 2, cls.WINDOW_HEIGHT // 2)


class TrainingConstants:
    """
    NEAT training configuration constants.
    
    Chứa parameters cho quá trình training AI với NEAT algorithm,
    bao gồm population size, generations, và difficulty-specific configs.
    """
    
    # Base training parameters
    DEFAULT_POPULATION_SIZE: int = 50
    FITNESS_THRESHOLD: float = 400.0
    
    # Difficulty-specific configurations
    DIFFICULTY_CONFIGS: Dict[str, Dict] = {
        'easy': {
            'generations': 10,
            'pop_size': 30,
            'fitness_threshold': 300,
            'hidden_nodes': 0,
            'model_filename': 'ai_easy.pkl',
            'description': 'Quick training, basic AI'
        },
        'medium': {
            'generations': 25,
            'pop_size': 50,
            'fitness_threshold': 400,
            'hidden_nodes': 2,
            'model_filename': 'ai_medium.pkl',
            'description': 'Balanced training, competent AI'
        },
        'hard': {
            'generations': 50,
            'pop_size': 75,
            'fitness_threshold': 500,
            'hidden_nodes': 4,
            'model_filename': 'ai_hard.pkl',
            'description': 'Intensive training, expert AI'
        }
    }
    
    # Neural network configuration
    NUM_INPUTS: int = 5   # ball_x, ball_y, ball_vx, ball_vy, paddle_y (normalized)
    NUM_OUTPUTS: int = 1  # continuous output [-1, 1] for paddle movement
    
    # Mutation rates
    WEIGHT_MUTATE_RATE: float = 0.8
    WEIGHT_REPLACE_RATE: float = 0.1
    NODE_ADD_PROB: float = 0.2
    NODE_DELETE_PROB: float = 0.2
    CONN_ADD_PROB: float = 0.5
    CONN_DELETE_PROB: float = 0.5
    
    # Directories
    MODELS_DIR: str = "models"
    LOGS_DIR: str = "logs"
    CONFIG_DIR: str = "config"
    
    @classmethod
    def get_difficulty_config(cls, difficulty: str) -> Dict:
        """
        Lấy configuration cho difficulty level cụ thể.
        
        Args:
            difficulty: 'easy', 'medium', hoặc 'hard'
            
        Returns:
            Dictionary chứa config cho difficulty đó
            
        Raises:
            ValueError: Nếu difficulty không hợp lệ
        """
        if difficulty not in cls.DIFFICULTY_CONFIGS:
            valid = list(cls.DIFFICULTY_CONFIGS.keys())
            raise ValueError(f"Invalid difficulty '{difficulty}'. Must be one of: {valid}")
        return cls.DIFFICULTY_CONFIGS[difficulty].copy()


class UIConstants:
    """
    UI và visual constants.
    
    Chứa tất cả constants liên quan đến user interface:
    - Colors (RGB tuples)
    - Font sizes
    - UI element dimensions
    - Animation parameters
    """
    
    # Color palette (RGB)
    COLOR_BLACK: Tuple[int, int, int] = (0, 0, 0)
    COLOR_WHITE: Tuple[int, int, int] = (255, 255, 255)
    COLOR_RED: Tuple[int, int, int] = (255, 0, 0)
    COLOR_GREEN: Tuple[int, int, int] = (0, 255, 0)
    COLOR_BLUE: Tuple[int, int, int] = (0, 0, 255)
    COLOR_YELLOW: Tuple[int, int, int] = (255, 255, 0)
    COLOR_CYAN: Tuple[int, int, int] = (0, 255, 255)
    COLOR_MAGENTA: Tuple[int, int, int] = (255, 0, 255)
    
    # Theme colors (Dark theme cho Pong)
    COLOR_BACKGROUND: Tuple[int, int, int] = (0, 0, 0)  # Black
    COLOR_PADDLE: Tuple[int, int, int] = (60, 40, 30)    # Dark brown
    COLOR_BALL: Tuple[int, int, int] = (50, 30, 20)      # Darker brown
    COLOR_TEXT: Tuple[int, int, int] = (255, 255, 255)   # White
    COLOR_SCORE: Tuple[int, int, int] = (50, 30, 20)     # Dark brown
    
    # UI element colors
    COLOR_PLAYER_BADGE: Tuple[int, int, int] = (100, 200, 255)  # Light blue
    COLOR_AI_BADGE: Tuple[int, int, int] = (255, 100, 100)      # Light red
    COLOR_BUTTON_HOVER: Tuple[int, int, int] = (150, 150, 150)  # Light gray
    COLOR_BUTTON_NORMAL: Tuple[int, int, int] = (100, 100, 100) # Gray
    
    # Font sizes
    FONT_SIZE_TITLE: int = 60
    FONT_SIZE_LARGE: int = 50
    FONT_SIZE_MEDIUM: int = 40
    FONT_SIZE_SMALL: int = 30
    FONT_SIZE_TINY: int = 20
    
    # Font names
    FONT_PRIMARY: str = "comicsans"
    FONT_FALLBACK: str = None  # None = pygame default
    
    # Menu settings
    MENU_BUTTON_WIDTH: int = 300
    MENU_BUTTON_HEIGHT: int = 60
    MENU_BUTTON_SPACING: int = 20
    MENU_TITLE_Y_OFFSET: int = 100
    
    # Badge dimensions
    BADGE_WIDTH: int = 160
    BADGE_HEIGHT: int = 50
    BADGE_Y_POSITION: int = 30
    
    # Animation parameters
    GLOW_LAYERS: int = 5           # Number of glow layers
    GLOW_MAX_ALPHA: int = 40       # Maximum alpha for glow
    BUTTON_SCALE_FACTOR: float = 0.05  # Scale increase on hover
    BUTTON_HOVER_SPEED: float = 0.1    # Hover animation speed
    
    # Screen effects
    SHAKE_DURATION: int = 10       # Frames
    SHAKE_MAGNITUDE: int = 5       # Pixels
    OVERLAY_ALPHA: int = 180       # Transparency for overlays
    
    # Particle effects
    PARTICLE_COUNT: int = 20       # Particles per effect
    PARTICLE_LIFETIME: int = 60    # Frames
    PARTICLE_SPEED_MIN: float = 1.0
    PARTICLE_SPEED_MAX: float = 3.0


class PowerUpConstants:
    """
    Power-up system constants.
    
    Chứa configuration cho power-up mechanics:
    - Spawn rates
    - Effect durations
    - Modifiers
    """
    
    # Spawn settings
    SPAWN_INTERVAL: int = 10       # Spawn every N total hits
    LIFETIME: int = 300            # Frames (5 seconds at 60 FPS)
    SIZE: int = 20                 # Pixel dimensions
    
    # Power-up types và effects
    POWER_UP_TYPES: Dict[str, Dict] = {
        'speed_boost': {
            'color': (255, 100, 100),  # Red
            'effect': 'ball_speed',
            'modifier': 1.5,           # 50% faster
            'duration': 180,           # 3 seconds
            'icon': '⚡'
        },
        'slow_motion': {
            'color': (100, 100, 255),  # Blue
            'effect': 'ball_speed',
            'modifier': 0.7,           # 30% slower
            'duration': 180,
            'icon': '❄'
        },
        'big_paddle': {
            'color': (100, 255, 100),  # Green
            'effect': 'paddle_height',
            'modifier': 1.5,           # 50% taller
            'duration': 240,           # 4 seconds
            'icon': '⬆'
        },
        'small_paddle': {
            'color': (255, 255, 100),  # Yellow
            'effect': 'paddle_height',
            'modifier': 0.7,           # 30% shorter
            'duration': 240,
            'icon': '⬇'
        }
    }
    
    # Probabilities (must sum to 1.0)
    POWER_UP_PROBABILITIES: Dict[str, float] = {
        'speed_boost': 0.25,
        'slow_motion': 0.25,
        'big_paddle': 0.25,
        'small_paddle': 0.25
    }


# Validation functions
def validate_constants() -> bool:
    """
    Validate tất cả constants để đảm bảo consistency.
    
    Kiểm tra:
    - Window dimensions hợp lệ
    - Paddle fit trong window
    - Probabilities sum to 1.0
    - No negative values
    
    Returns:
        True nếu tất cả constants hợp lệ
        
    Raises:
        ValueError: Nếu phát hiện invalid constants
    """
    errors = []
    
    # Check window dimensions
    if GameConstants.WINDOW_WIDTH <= 0 or GameConstants.WINDOW_HEIGHT <= 0:
        errors.append("Window dimensions must be positive")
    
    # Check paddle fits in window
    if GameConstants.PADDLE_HEIGHT > GameConstants.WINDOW_HEIGHT:
        errors.append("Paddle height exceeds window height")
    
    # Check power-up probabilities
    total_prob = sum(PowerUpConstants.POWER_UP_PROBABILITIES.values())
    if abs(total_prob - 1.0) > 0.01:  # Allow small floating point error
        errors.append(f"Power-up probabilities must sum to 1.0, got {total_prob}")
    
    # Check training configs
    for difficulty, config in TrainingConstants.DIFFICULTY_CONFIGS.items():
        if config['generations'] <= 0:
            errors.append(f"Invalid generations for {difficulty}")
        if config['pop_size'] <= 0:
            errors.append(f"Invalid population size for {difficulty}")
    
    if errors:
        raise ValueError("Constant validation failed:\n" + "\n".join(errors))
    
    return True


# Run validation on import
if __name__ == "__main__":
    print("Validating constants...")
    try:
        validate_constants()
        print("✓ All constants are valid!")
    except ValueError as e:
        print(f"✗ Validation failed:\n{e}")
