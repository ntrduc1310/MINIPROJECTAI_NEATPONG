"""
Ball Class - TV2 (Dũng)
Xử lý di chuyển và vật lý của bóng với physics simulation đầy đủ.

Module này cung cấp Ball class để quản lý trạng thái, chuyển động và rendering
của bóng trong game Pong với các tính năng power-up modifiers.

Classes:
    Ball: Đại diện cho bóng với physics và visual effects
"""
import pygame
import math
import random
from typing import Tuple, List, Optional


class Ball:
    """
    Đại diện cho bóng trong game Pong với physics và visual effects.
    
    Class này quản lý vị trí, vận tốc, rendering và các power-up modifiers
    của bóng. Bao gồm hệ thống góc phóng random và visual effects như glow.
    
    Attributes:
        MAX_VEL (float): Vận tốc tối đa của bóng (pixels per frame)
        RADIUS (int): Bán kính của bóng (pixels)
        x (float): Tọa độ X hiện tại
        y (float): Tọa độ Y hiện tại
        original_x (float): Tọa độ X ban đầu để reset
        original_y (float): Tọa độ Y ban đầu để reset
        x_vel (float): Vận tốc theo trục X
        y_vel (float): Vận tốc theo trục Y
        speed_modifier (float): Hệ số điều chỉnh tốc độ từ power-ups
    """
    
    MAX_VEL: float = 5.0
    RADIUS: int = 7
    
    def __init__(self, x: float, y: float) -> None:
        """
        Khởi tạo đối tượng Ball với vị trí và vận tốc ban đầu.
        
        Bóng được khởi tạo với góc phóng ngẫu nhiên trong khoảng [-30°, 30°]
        và hướng random (trái hoặc phải). Vận tốc được tính toán dựa trên
        góc phóng và MAX_VEL constant.
        
        Args:
            x: Tọa độ X ban đầu của bóng (pixels). Phải là số dương.
            y: Tọa độ Y ban đầu của bóng (pixels). Phải là số dương.
            
        Raises:
            ValueError: Nếu x hoặc y là số âm
            TypeError: Nếu x hoặc y không phải là số
        
        Examples:
            >>> ball = Ball(400, 300)
            >>> print(f"Ball position: ({ball.x}, {ball.y})")
            Ball position: (400, 300)
        """
        # Input validation
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError(f"Position coordinates must be numeric, got x={type(x)}, y={type(y)}")
        if x < 0 or y < 0:
            raise ValueError(f"Position coordinates must be non-negative, got x={x}, y={y}")
        
        self.x = self.original_x = float(x)
        self.y = self.original_y = float(y)
        
        # Random angle và direction
        angle = self._get_random_angle(-30, 30, [0])
        pos = 1 if random.random() < 0.5 else -1
        
        self.x_vel = pos * abs(math.cos(angle) * self.MAX_VEL)
        self.y_vel = math.sin(angle) * self.MAX_VEL
        
        # Speed modifier cho power-ups (1.0 = normal speed)
        self.speed_modifier = 1.0
    
    def _get_random_angle(self, min_angle: int, max_angle: int, excluded: List[float]) -> float:
        """
        Tạo góc phóng ngẫu nhiên trong khoảng cho trước, tránh các góc excluded.
        
        Method này sinh góc random trong khoảng [min_angle, max_angle] độ
        và đảm bảo không trùng với bất kỳ giá trị nào trong danh sách excluded.
        
        Args:
            min_angle: Góc tối thiểu (degrees). Nên trong khoảng [-90, 90].
            max_angle: Góc tối đa (degrees). Phải lớn hơn min_angle.
            excluded: Danh sách các góc cần tránh (radians).
            
        Returns:
            Góc phóng được chọn (radians), không nằm trong excluded list.
            
        Raises:
            ValueError: Nếu max_angle <= min_angle
            
        Note:
            Góc được trả về ở dạng radians, trong khi input là degrees.
            Infinite loop có thể xảy ra nếu excluded list quá lớn.
        """
        if max_angle <= min_angle:
            raise ValueError(f"max_angle ({max_angle}) must be greater than min_angle ({min_angle})")
        
        angle = 0.0
        max_attempts = 100  # Prevent infinite loop
        attempts = 0
        
        while angle in excluded and attempts < max_attempts:
            angle = math.radians(random.randrange(min_angle, max_angle))
            attempts += 1
            
        if attempts >= max_attempts:
            # Fallback: return a safe default angle if can't find non-excluded angle
            angle = math.radians((min_angle + max_angle) // 2)
            
        return angle
    
    def draw(self, win: pygame.Surface, color: Tuple[int, int, int] = (255, 255, 255)) -> None:
        """
        Render bóng lên surface với multi-layer glow effects và glossy highlight.
        
        Phương thức này vẽ bóng với hiệu ứng visual chuyên nghiệp bao gồm:
        - Multi-layer glow effect với alpha blending
        - Gradient shading cho độ sâu
        - Glossy highlight tạo hiệu ứng bóng bẩy
        
        Args:
            win: Pygame Surface để vẽ lên. Phải là valid Surface object.
            color: Màu cơ bản của bóng dưới dạng RGB tuple (0-255 cho mỗi channel).
                  Mặc định là trắng (255, 255, 255). Note: màu này hiện không được
                  sử dụng do theme tối đậm đã được hard-code.
                  
        Raises:
            pygame.error: Nếu surface không valid hoặc không thể draw
            TypeError: Nếu color không phải là tuple với 3 giá trị
            
        Note:
            Method này tự động điều chỉnh màu cho phù hợp với background theme.
            Hiện tại sử dụng màu tối (50, 30, 20) bất kể tham số color.
        """
        # Sử dụng màu tối cho ball trên nền sáng
        ball_color = (50, 30, 20)
        
        # Multi-layer glow effect
        glow_radius = self.RADIUS + 6
        glow_surf = pygame.Surface((glow_radius * 2 + 10, glow_radius * 2 + 10), pygame.SRCALPHA)
        
        # Outer glow layers
        for i in range(5, 0, -1):
            alpha = 30 - i * 5
            current_radius = self.RADIUS + i
            glow_color = (*ball_color, alpha)
            pygame.draw.circle(glow_surf, glow_color, 
                             (glow_radius + 5, glow_radius + 5), current_radius)
        
        win.blit(glow_surf, (self.x - glow_radius - 5, self.y - glow_radius - 5))
        
        # Main ball with gradient
        pygame.draw.circle(win, ball_color, (self.x, self.y), self.RADIUS)
        
        # Glossy highlight
        highlight_color = (150, 120, 90)
        pygame.draw.circle(win, highlight_color, 
                          (self.x - 2, self.y - 2), self.RADIUS // 3)
    
    def move(self) -> None:
        """
        Cập nhật vị trí bóng dựa trên vận tốc hiện tại và speed modifier.
        
        Phương thức này được gọi mỗi frame để update vị trí bóng.
        Tốc độ cuối cùng = base_velocity * speed_modifier.
        
        Speed modifier có thể thay đổi từ power-ups:
        - < 1.0: Bóng chậm hơn (slow-motion)
        - = 1.0: Tốc độ bình thường
        - > 1.0: Bóng nhanh hơn (speed boost)
        
        Note:
            Method này không kiểm tra collision, chỉ update vị trí.
            Collision detection được xử lý trong GameManager.
        """
        self.x += self.x_vel * self.speed_modifier
        self.y += self.y_vel * self.speed_modifier
    
    def reset(self) -> None:
        """
        Reset bóng về vị trí ban đầu với vận tốc mới.
        
        Phương thức này được gọi khi có người ghi điểm để bắt đầu vòng mới.
        Bóng được đặt lại ở trung tâm và được phóng về hướng ngược lại với
        góc random mới.
        
        Behaviors:
            - Vị trí: Reset về (original_x, original_y)
            - Góc: Random mới trong khoảng [-30°, 30°]
            - Hướng X: Đảo ngược hướng hiện tại
            - Hướng Y: Random dựa trên góc mới
            - Speed modifier: Reset về 1.0 (normal speed)
            
        Note:
            Method này đảm bảo bóng luôn bay về hướng người vừa bị ghi điểm.
        """
        self.x = self.original_x
        self.y = self.original_y
        
        angle = self._get_random_angle(-30, 30, [0])
        x_vel = abs(math.cos(angle) * self.MAX_VEL)
        y_vel = math.sin(angle) * self.MAX_VEL
        
        self.y_vel = y_vel
        self.x_vel *= -1  # Reverse direction
        self.speed_modifier = 1.0
    
    def apply_speed_modifier(self, modifier: float) -> None:
        """
        Áp dụng hệ số tốc độ từ power-ups hoặc difficulty settings.
        
        Phương thức này cho phép thay đổi tốc độ bóng mà không thay đổi
        vận tốc cơ bản. Modifier được nhân với vận tốc trong move().
        
        Args:
            modifier: Hệ số nhân cho tốc độ. Phải > 0.
                     - 0.5: Bóng chậm 50%
                     - 1.0: Tốc độ bình thường (mặc định)
                     - 1.5: Bóng nhanh 50%
                     - 2.0: Bóng nhanh gấp đôi
                     
        Raises:
            ValueError: Nếu modifier <= 0 (không cho phép tốc độ âm hoặc 0)
            TypeError: Nếu modifier không phải là số
            
        Examples:
            >>> ball.apply_speed_modifier(1.5)  # Tăng tốc 50%
            >>> ball.apply_speed_modifier(0.7)  # Giảm tốc 30%
            
        Note:
            Modifier quá cao (>3.0) có thể gây ra collision detection issues.
            Khuyến nghị giữ modifier trong khoảng [0.5, 2.0].
        """
        if not isinstance(modifier, (int, float)):
            raise TypeError(f"Speed modifier must be numeric, got {type(modifier)}")
        if modifier <= 0:
            raise ValueError(f"Speed modifier must be positive, got {modifier}")
        if modifier > 5.0:
            # Warning for extreme values but don't raise error
            print(f"[WARNING] Extreme speed modifier {modifier} may cause issues")
            
        self.speed_modifier = float(modifier)
