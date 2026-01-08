"""
Paddle Class - TV2 (Dũng)
Xử lý vợt và di chuyển với hỗ trợ power-up modifiers.

Module này cung cấp Paddle class để quản lý trạng thái, chuyển động,
rendering và modifiers của vợt người chơi/AI trong game Pong.

Classes:
    Paddle: Đại diện cho vợt với visual effects và modifiers
"""
import pygame
from typing import Tuple, Optional


class Paddle:
    """
    Đại diện cho vợt trong game Pong với power-up modifiers.
    
    Class này quản lý vị trí, kích thước, chuyển động và rendering của vợt.
    Hỗ trợ dynamic height và speed modifiers từ hệ thống power-ups.
    
    Attributes:
        VEL (float): Vận tốc cơ bản của vợt (pixels per frame)
        WIDTH (int): Chiều rộng vợt (pixels)
        HEIGHT (int): Chiều cao cơ bản của vợt (pixels)
        x (float): Tọa độ X hiện tại
        y (float): Tọa độ Y hiện tại
        original_x (float): Tọa độ X ban đầu để reset
        original_y (float): Tọa độ Y ban đầu để reset
        height_modifier (float): Hệ số điều chỉnh chiều cao (1.0 = normal)
        speed_modifier (float): Hệ số điều chỉnh tốc độ (1.0 = normal)
    """
    
    VEL: float = 4.0
    WIDTH: int = 20
    HEIGHT: int = 100
    
    def __init__(self, x: float, y: float) -> None:
        """
        Khởi tạo đối tượng Paddle với vị trí ban đầu.
        
        Args:
            x: Tọa độ X ban đầu của vợt (pixels). Phải là số không âm.
            y: Tọa độ Y ban đầu của vợt (pixels). Phải là số không âm.
            
        Raises:
            ValueError: Nếu x hoặc y là số âm
            TypeError: Nếu x hoặc y không phải là số
            
        Note:
            Modifiers được khởi tạo ở 1.0 (giá trị bình thường, không thay đổi).
        """
        # Input validation
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError(f"Position coordinates must be numeric, got x={type(x)}, y={type(y)}")
        if x < 0 or y < 0:
            raise ValueError(f"Position coordinates must be non-negative, got x={x}, y={y}")
        
        self.x = self.original_x = float(x)
        self.y = self.original_y = float(y)
        
        # Modifiers cho power-ups (1.0 = no modification)
        self.height_modifier = 1.0
        self.speed_modifier = 1.0
    
    def draw(self, win: pygame.Surface, color: Tuple[int, int, int] = (255, 255, 255)) -> None:
        """
        Render vợt lên surface với gradient và glow effects.
        
        Vẽ vợt với visual effects chuyên nghiệp bao gồm glow effect
        và highlight edge. Chiều cao được điều chỉnh theo height_modifier.
        
        Args:
            win: Pygame Surface để vẽ lên. Phải là valid Surface object.
            color: Màu vợt dưới dạng RGB tuple (0-255 cho mỗi channel).
                  Mặc định là trắng (255, 255, 255). Note: tham số này
                  hiện không được sử dụng do theme tối đã hard-code.
                  
        Note:
            - Chiều cao thực tế = HEIGHT * height_modifier
            - Màu được hard-code là (60, 40, 30) cho theme tối
            - Glow effect tự động scale theo chiều cao
        """
        current_height = int(self.HEIGHT * self.height_modifier)
        
        # Sử dụng màu tối đậm cho vợt trên nền sáng
        paddle_color = (60, 40, 30)
        
        # Glow effect sáng
        glow_surf = pygame.Surface((self.WIDTH + 12, current_height + 12), pygame.SRCALPHA)
        for i in range(3):
            glow_alpha = 40 - i * 10
            glow_color = (*paddle_color, glow_alpha)
            pygame.draw.rect(glow_surf, glow_color, 
                           (i, i, self.WIDTH + 12 - 2*i, current_height + 12 - 2*i), 
                           border_radius=8)
        win.blit(glow_surf, (self.x - 6, self.y - 6))
        
        # Main paddle body
        pygame.draw.rect(win, paddle_color, 
                        (self.x, self.y, self.WIDTH, current_height), 
                        border_radius=6)
        
        # Highlight edge
        highlight_color = (100, 80, 60)
        pygame.draw.rect(win, highlight_color, 
                        (self.x, self.y, self.WIDTH, current_height), 
                        3, border_radius=6)
    
    def move(self, up: bool = True) -> None:
        """
        Di chuyển vợt theo hướng chỉ định.
        
        Tốc độ di chuyển = VEL * speed_modifier. Method này chỉ update
        vị trí, không kiểm tra boundary (kiểm tra boundary trong GameManager).
        
        Args:
            up: True để di chuyển lên (giảm Y), False để di chuyển xuống (tăng Y).
                Mặc định là True.
                
        Note:
            - Trong pygame, Y tăng khi xuống, giảm khi lên
            - Speed modifier ảnh hưởng trực tiếp đến vận tốc
            - Không có boundary check, có thể di chuyển ra ngoài màn hình
        """
        vel = self.VEL * self.speed_modifier
        if up:
            self.y -= vel
        else:
            self.y += vel
    
    def reset(self) -> None:
        """
        Reset vợt về trạng thái ban đầu.
        
        Đặt lại vị trí về original position và reset tất cả modifiers
        về giá trị mặc định (1.0).
        
        Note:
            Được gọi khi bắt đầu game mới hoặc sau khi có người thắng.
        """
        self.x = self.original_x
        self.y = self.original_y
        self.height_modifier = 1.0
        self.speed_modifier = 1.0
    
    def get_current_height(self) -> int:
        """
        Lấy chiều cao hiện tại của vợt (có tính modifier).
        
        Returns:
            Chiều cao hiện tại tính bằng pixels (HEIGHT * height_modifier),
            được làm tròn thành số nguyên.
            
        Examples:
            >>> paddle = Paddle(10, 100)
            >>> paddle.height_modifier = 1.5
            >>> paddle.get_current_height()
            150
        """
        return int(self.HEIGHT * self.height_modifier)
    
    def apply_height_modifier(self, modifier: float) -> None:
        """
        Áp dụng modifier cho chiều cao vợt.
        
        Args:
            modifier: Hệ số nhân cho chiều cao. Phải > 0.
                     - 0.5: Vợt ngắn hơn 50%
                     - 1.0: Chiều cao bình thường
                     - 1.5: Vợt cao hơn 50%
                     
        Raises:
            ValueError: Nếu modifier <= 0
            TypeError: Nếu modifier không phải số
        """
        if not isinstance(modifier, (int, float)):
            raise TypeError(f"Height modifier must be numeric, got {type(modifier)}")
        if modifier <= 0:
            raise ValueError(f"Height modifier must be positive, got {modifier}")
            
        self.height_modifier = float(modifier)
    
    def apply_speed_modifier(self, modifier: float) -> None:
        """
        Áp dụng modifier cho tốc độ di chuyển vợt.
        
        Args:
            modifier: Hệ số nhân cho tốc độ. Phải > 0.
                     - 0.5: Vợt chậm hơn 50%
                     - 1.0: Tốc độ bình thường
                     - 1.5: Vợt nhanh hơn 50%
                     
        Raises:
            ValueError: Nếu modifier <= 0
            TypeError: Nếu modifier không phải số
        """
        if not isinstance(modifier, (int, float)):
            raise TypeError(f"Speed modifier must be numeric, got {type(modifier)}")
        if modifier <= 0:
            raise ValueError(f"Speed modifier must be positive, got {modifier}")
            
        self.speed_modifier = float(modifier)
