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
        """Vẽ điểm số với modern styling"""
        # Player labels
        label_font = pygame.font.Font(None, 28)
        player_label = label_font.render("< YOU", True, (100, 200, 255))
        ai_label = label_font.render("AI >", True, (255, 100, 100))
        
        self.window.blit(player_label, 
                        (self.window_width // 4 - player_label.get_width() // 2, 15))
        self.window.blit(ai_label, 
                        (self.window_width * 3 // 4 - ai_label.get_width() // 2, 15))
        
        # Scores with shadow
        left_color = (100, 200, 255)
        right_color = (255, 100, 100)
        
        # Left score
        shadow_left = self.SCORE_FONT.render(f"{self.left_score}", True, (0, 0, 0))
        left_score_text = self.SCORE_FONT.render(f"{self.left_score}", True, left_color)
        left_x = self.window_width // 4 - left_score_text.get_width() // 2
        self.window.blit(shadow_left, (left_x + 2, 52))
        self.window.blit(left_score_text, (left_x, 50))
        
        # Right score
        shadow_right = self.SCORE_FONT.render(f"{self.right_score}", True, (0, 0, 0))
        right_score_text = self.SCORE_FONT.render(f"{self.right_score}", True, right_color)
        right_x = self.window_width * 3 // 4 - right_score_text.get_width() // 2
        self.window.blit(shadow_right, (right_x + 2, 52))
        self.window.blit(right_score_text, (right_x, 50))
    
    def _draw_hits(self):
        """Vẽ số hits với background"""
        total_hits = self.left_hits + self.right_hits
        
        # Background box
        box_width = 120
        box_height = 35
        box_x = self.window_width // 2 - box_width // 2
        box_y = self.window_height - 50
        
        # Semi-transparent background
        bg_surf = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surf, (30, 30, 50, 180), bg_surf.get_rect(), border_radius=8)
        self.window.blit(bg_surf, (box_x, box_y))
        
        # Hits text
        hits_font = pygame.font.Font(None, 28)
        hits_text = hits_font.render(f"HITS: {total_hits}", True, (255, 220, 100))
        self.window.blit(hits_text, 
                        (self.window_width // 2 - hits_text.get_width() // 2, box_y + 8))
    
    def _draw_divider(self):
        """Vẽ đường chia giữa với modern style"""
        center_x = self.window_width // 2
        dash_height = 15
        dash_spacing = 30
        
        for i in range(0, self.window_height, dash_spacing):
            # Gradient color based on position
            progress = i / self.window_height
            alpha = int(120 + 60 * abs(0.5 - progress))
            color = (80, 150, 200) if i % 60 == 0 else (60, 120, 180)
            
            pygame.draw.rect(
                self.window, color,
                (center_x - 2, i, 4, dash_height)
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
            bg_color: Màu background (None = gradient)
        """
        if bg_color:
            self.window.fill(bg_color)
        else:
            # Gradient background
            for y in range(self.window_height):
                progress = y / self.window_height
                color = (
                    int(5 + 10 * progress),
                    int(10 + 15 * progress),
                    int(20 + 25 * progress)
                )
                pygame.draw.line(self.window, color, (0, y), (self.window_width, y))
        
        self._draw_divider()
        
        if draw_score:
            self._draw_score()
        
        if draw_hits:
            self._draw_hits()
        
        # Vẽ game objects với màu đẹp hơn
        self.left_paddle.draw(self.window, color=(100, 200, 255))  # Blue for player
        self.right_paddle.draw(self.window, color=(255, 100, 100))  # Red for AI
        self.ball.draw(self.window, color=(255, 255, 255))  # White ball
    
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
        vel = paddle.VEL * paddle.speed_modifier
        
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
