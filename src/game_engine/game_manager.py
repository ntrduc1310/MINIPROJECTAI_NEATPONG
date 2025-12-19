"""
Game Manager - TV2 (Dũng)
Quản lý điểm số, va chạm và game state
"""
import pygame
from .ball import Ball
from .paddle import Paddle


class GameInfo:
    """Thông tin game state"""
    
    def __init__(self, left_hits, right_hits, left_score, right_score):
        self.left_hits = left_hits
        self.right_hits = right_hits
        self.left_score = left_score
        self.right_score = right_score


class GameManager:
    """
    Quản lý logic game chính
    - Va chạm
    - Điểm số
    - Drawing
    """
    
    SCORE_FONT = None  # Will be initialized later
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    
    def __init__(self, window, window_width, window_height):
        """
        Khởi tạo game manager
        
        Args:
            window: Pygame window
            window_width: Chiều rộng window
            window_height: Chiều cao window
        """
        self.window_width = window_width
        self.window_height = window_height
        self.window = window
        
        # Initialize font if not yet done
        if GameManager.SCORE_FONT is None:
            try:
                GameManager.SCORE_FONT = pygame.font.SysFont("comicsans", 50)
            except:
                GameManager.SCORE_FONT = pygame.font.Font(None, 50)
        
        # Tạo game objects
        self.left_paddle = Paddle(10, window_height // 2 - Paddle.HEIGHT // 2)
        self.right_paddle = Paddle(
            window_width - 10 - Paddle.WIDTH, 
            window_height // 2 - Paddle.HEIGHT // 2
        )
        self.ball = Ball(window_width // 2, window_height // 2)
        
        # Game state
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0
    
    def _draw_score(self):
        """Vẽ điểm số"""
        left_score_text = self.SCORE_FONT.render(f"{self.left_score}", 1, self.WHITE)
        right_score_text = self.SCORE_FONT.render(f"{self.right_score}", 1, self.WHITE)
        
        self.window.blit(left_score_text, 
                        (self.window_width // 4 - left_score_text.get_width() // 2, 20))
        self.window.blit(right_score_text, 
                        (self.window_width * 3 // 4 - right_score_text.get_width() // 2, 20))
    
    def _draw_hits(self):
        """Vẽ số hits"""
        hits_text = self.SCORE_FONT.render(
            f"{self.left_hits + self.right_hits}", 1, self.RED
        )
        self.window.blit(hits_text, 
                        (self.window_width // 2 - hits_text.get_width() // 2, 10))
    
    def _draw_divider(self):
        """Vẽ đường chia giữa"""
        for i in range(10, self.window_height, self.window_height // 20):
            if i % 2 == 1:
                continue
            pygame.draw.rect(
                self.window, self.WHITE, 
                (self.window_width // 2 - 5, i, 10, self.window_height // 20)
            )
    
    def handle_collision(self):
        """
        Xử lý va chạm bóng với tường và vợt
        
        Returns:
            bool: True nếu có va chạm với vợt
        """
        ball = self.ball
        left_paddle = self.left_paddle
        right_paddle = self.right_paddle
        
        paddle_collision = False
        
        # Va chạm tường trên/dưới
        if ball.y + ball.RADIUS >= self.window_height:
            ball.y_vel *= -1
        elif ball.y - ball.RADIUS <= 0:
            ball.y_vel *= -1
        
        # Va chạm vợt trái
        if ball.x_vel < 0:
            paddle_height = left_paddle.get_current_height()
            if ball.y >= left_paddle.y and ball.y <= left_paddle.y + paddle_height:
                if ball.x - ball.RADIUS <= left_paddle.x + Paddle.WIDTH:
                    ball.x_vel *= -1
                    
                    # Tính góc bounce dựa trên vị trí hit
                    middle_y = left_paddle.y + paddle_height / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (paddle_height / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel
                    
                    self.left_hits += 1
                    paddle_collision = True
        
        # Va chạm vợt phải
        else:
            paddle_height = right_paddle.get_current_height()
            if ball.y >= right_paddle.y and ball.y <= right_paddle.y + paddle_height:
                if ball.x + ball.RADIUS >= right_paddle.x:
                    ball.x_vel *= -1
                    
                    # Tính góc bounce
                    middle_y = right_paddle.y + paddle_height / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (paddle_height / 2) / ball.MAX_VEL
                    y_vel = difference_in_y / reduction_factor
                    ball.y_vel = -1 * y_vel
                    
                    self.right_hits += 1
                    paddle_collision = True
        
        return paddle_collision
    
    def draw(self, draw_score=True, draw_hits=False, bg_color=None):
        """
        Vẽ toàn bộ game
        
        Args:
            draw_score: Vẽ điểm số
            draw_hits: Vẽ số hits
            bg_color: Màu background (None = BLACK)
        """
        bg = bg_color if bg_color else self.BLACK
        self.window.fill(bg)
        
        self._draw_divider()
        
        if draw_score:
            self._draw_score()
        
        if draw_hits:
            self._draw_hits()
        
        # Vẽ game objects
        self.left_paddle.draw(self.window)
        self.right_paddle.draw(self.window)
        self.ball.draw(self.window)
    
    def move_paddle(self, left=True, up=True):
        """
        Di chuyển vợt với boundary checking
        
        Args:
            left: True = vợt trái, False = vợt phải
            up: True = lên, False = xuống
        
        Returns:
            bool: True nếu di chuyển hợp lệ
        """
        paddle = self.left_paddle if left else self.right_paddle
        paddle_height = paddle.get_current_height()
        vel = Paddle.VEL * paddle.speed_modifier
        
        if left:
            if up and paddle.y - vel < 0:
                return False
            if not up and paddle.y + paddle_height > self.window_height:
                return False
            paddle.move(up)
        else:
            if up and paddle.y - vel < 0:
                return False
            if not up and paddle.y + paddle_height > self.window_height:
                return False
            paddle.move(up)
        
        return True
    
    def loop(self):
        """
        Game loop chính
        
        Returns:
            GameInfo: Thông tin game hiện tại
        """
        self.ball.move()
        self.handle_collision()
        
        # Check scoring
        if self.ball.x < 0:
            self.ball.reset()
            self.right_score += 1
        elif self.ball.x > self.window_width:
            self.ball.reset()
            self.left_score += 1
        
        return GameInfo(
            self.left_hits, self.right_hits, 
            self.left_score, self.right_score
        )
    
    def reset(self):
        """Reset game về trạng thái ban đầu"""
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0
