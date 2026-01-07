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
        """Vẽ điểm số với modern styling - badges đẹp với icons"""
        # Draw Player Badge (YOU) - Left side
        badge_width = 160
        badge_height = 50
        left_x = self.window_width // 4
        badge_y = 30
        
        # Player badge
        self._draw_player_badge(left_x, badge_y, badge_width, badge_height, 
                               "PLAYER", (100, 200, 255))
        
        # AI badge  
        right_x = self.window_width * 3 // 4
        self._draw_ai_badge(right_x, badge_y, 140, badge_height,
                           "AI", (255, 100, 100))
        
        # Scores với màu tối và shadow (đặt ở vị trí thấp hơn badges)
        left_color = (50, 30, 20)
        right_color = (50, 30, 20)
        
        score_y = 75  # Vị trí score thấp hơn badge
        
        # Left score
        shadow_left = self.SCORE_FONT.render(f"{self.left_score}", True, (255, 255, 255, 100))
        left_score_text = self.SCORE_FONT.render(f"{self.left_score}", True, left_color)
        left_x_pos = self.window_width // 4 - left_score_text.get_width() // 2
        self.window.blit(shadow_left, (left_x_pos + 3, score_y + 3))
        self.window.blit(left_score_text, (left_x_pos, score_y))
        
        # Right score
        shadow_right = self.SCORE_FONT.render(f"{self.right_score}", True, (255, 255, 255, 100))
        right_score_text = self.SCORE_FONT.render(f"{self.right_score}", True, right_color)
        right_x_pos = self.window_width * 3 // 4 - right_score_text.get_width() // 2
        self.window.blit(shadow_right, (right_x_pos + 3, score_y + 3))
        self.window.blit(right_score_text, (right_x_pos, score_y))
    
    def _draw_player_badge(self, x, y, width, height, text, border_color):
        """Vẽ badge đẹp cho Player với icon"""
        badge_x = x - width // 2
        badge_y = y - height // 2
        
        # Outer glow
        glow_surf = pygame.Surface((width + 10, height + 10), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*border_color, 80), glow_surf.get_rect(), border_radius=15)
        self.window.blit(glow_surf, (badge_x - 5, badge_y - 5))
        
        # Main badge background
        pygame.draw.rect(self.window, (255, 255, 255), 
                        (badge_x, badge_y, width, height), border_radius=12)
        
        # Border
        pygame.draw.rect(self.window, border_color, 
                        (badge_x, badge_y, width, height), 3, border_radius=12)
        
        # Icon - Gamepad
        icon_x = badge_x + 15
        icon_y = badge_y + height // 2
        pygame.draw.circle(self.window, border_color, (icon_x, icon_y), 12)
        pygame.draw.circle(self.window, (255, 255, 255), (icon_x, icon_y), 10)
        pygame.draw.circle(self.window, border_color, (icon_x, icon_y), 8)
        # D-pad
        pygame.draw.rect(self.window, (255, 255, 255), (icon_x - 6, icon_y - 2, 12, 4))
        pygame.draw.rect(self.window, (255, 255, 255), (icon_x - 2, icon_y - 6, 4, 12))
        
        # Text with shadow
        font = pygame.font.Font(None, 32)
        text_color = (80, 60, 40)
        shadow = font.render(text, True, (50, 50, 50))
        text_surf = font.render(text, True, text_color)
        text_x = badge_x + 50
        text_y = badge_y + height // 2 - text_surf.get_height() // 2
        self.window.blit(shadow, (text_x + 2, text_y + 2))
        self.window.blit(text_surf, (text_x, text_y))
    
    def _draw_ai_badge(self, x, y, width, height, text, border_color):
        """Vẽ badge đẹp cho AI với icon chip"""
        badge_x = x - width // 2
        badge_y = y - height // 2
        
        # Outer glow
        glow_surf = pygame.Surface((width + 10, height + 10), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*border_color, 80), glow_surf.get_rect(), border_radius=15)
        self.window.blit(glow_surf, (badge_x - 5, badge_y - 5))
        
        # Main badge background
        pygame.draw.rect(self.window, (255, 255, 255), 
                        (badge_x, badge_y, width, height), border_radius=12)
        
        # Border
        pygame.draw.rect(self.window, border_color, 
                        (badge_x, badge_y, width, height), 3, border_radius=12)
        
        # Icon - AI Chip
        icon_x = badge_x + 25
        icon_y = badge_y + height // 2
        # Chip body
        pygame.draw.rect(self.window, border_color, (icon_x - 8, icon_y - 8, 16, 16), border_radius=2)
        pygame.draw.rect(self.window, (255, 255, 255), (icon_x - 6, icon_y - 6, 12, 12))
        # Circuit lines
        pygame.draw.line(self.window, border_color, (icon_x - 4, icon_y - 3), (icon_x + 4, icon_y - 3), 2)
        pygame.draw.line(self.window, border_color, (icon_x - 4, icon_y), (icon_x + 4, icon_y), 2)
        pygame.draw.line(self.window, border_color, (icon_x - 4, icon_y + 3), (icon_x + 4, icon_y + 3), 2)
        # Pins
        for i in [-1, 1]:
            pygame.draw.line(self.window, border_color, (icon_x + 8 * i, icon_y - 6), (icon_x + 11 * i, icon_y - 6), 2)
            pygame.draw.line(self.window, border_color, (icon_x + 8 * i, icon_y), (icon_x + 11 * i, icon_y), 2)
            pygame.draw.line(self.window, border_color, (icon_x + 8 * i, icon_y + 6), (icon_x + 11 * i, icon_y + 6), 2)
        
        # Text with shadow
        font = pygame.font.Font(None, 36)
        text_color = (80, 60, 40)
        shadow = font.render(text, True, (50, 50, 50))
        text_surf = font.render(text, True, text_color)
        text_x = badge_x + 55
        text_y = badge_y + height // 2 - text_surf.get_height() // 2
        self.window.blit(shadow, (text_x + 2, text_y + 2))
        self.window.blit(text_surf, (text_x, text_y))
    
    def _draw_hits(self):
        """Vẽ số hits với modern design"""
        total_hits = self.left_hits + self.right_hits
        
        # Background box với viền
        box_width = 140
        box_height = 45
        box_x = self.window_width // 2 - box_width // 2
        box_y = self.window_height - 60
        
        # White background with border
        pygame.draw.rect(self.window, (255, 255, 255), 
                        (box_x, box_y, box_width, box_height), border_radius=10)
        pygame.draw.rect(self.window, (80, 60, 40), 
                        (box_x, box_y, box_width, box_height), 3, border_radius=10)
        
        # Hits text
        hits_font = pygame.font.Font(None, 32)
        hits_text = hits_font.render(f"HITS: {total_hits}", True, (80, 60, 40))
        self.window.blit(hits_text, 
                        (self.window_width // 2 - hits_text.get_width() // 2, box_y + 10))
    
    def _draw_gradient_background(self):
        """Vẽ gradient background hiện đại (vàng-cam theo hình tham khảo)"""
        # Tạo gradient từ vàng sáng sang cam
        for y in range(self.window_height):
            progress = y / self.window_height
            # Màu vàng (255, 220, 100) -> cam (255, 160, 80)
            r = 255
            g = int(220 - (60 * progress))
            b = int(100 - (20 * progress))
            pygame.draw.line(self.window, (r, g, b), (0, y), (self.window_width, y))
    
    def _draw_divider(self):
        """Vẽ đường chia giữa với modern style"""
        center_x = self.window_width // 2
        dash_height = 20
        dash_spacing = 35
        line_width = 5
        
        for i in range(0, self.window_height, dash_spacing):
            # Màu trắng với độ mờ cao cho professional look
            pygame.draw.rect(
                self.window, (255, 255, 255),
                (center_x - line_width//2, i, line_width, dash_height),
                border_radius=3
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
            # Modern gradient background (yellow-orange like reference image)
            self._draw_gradient_background()
        
        self._draw_divider()
        
        if draw_score:
            self._draw_score()
        
        if draw_hits:
            self._draw_hits()
        
        # Vẽ game objects - không cần chỉ định màu, dùng default
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
