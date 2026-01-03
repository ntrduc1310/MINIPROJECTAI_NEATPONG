"""
Paddle Class - TV2 (Dũng)
Xử lý vợt và di chuyển
"""
import pygame


class Paddle:
    """Paddle với modifiers cho power-ups"""
    
    VEL = 4
    WIDTH = 20
    HEIGHT = 100
    
    def __init__(self, x, y):
        """
        Khởi tạo vợt
        
        Args:
            x: Vị trí X
            y: Vị trí Y
        """
        self.x = self.original_x = x
        self.y = self.original_y = y
        
        # Modifiers cho power-ups
        self.height_modifier = 1.0
        self.speed_modifier = 1.0
    
    def draw(self, win, color=(255, 255, 255)):
        """
        Vẽ vợt với gradient và glow
        
        Args:
            win: Pygame window
            color: Màu vợt (RGB tuple)
        """
        current_height = int(self.HEIGHT * self.height_modifier)
        
        # Glow effect
        glow_surf = pygame.Surface((self.WIDTH + 8, current_height + 8), pygame.SRCALPHA)
        glow_color = (*color, 60)
        pygame.draw.rect(glow_surf, glow_color, glow_surf.get_rect(), border_radius=6)
        win.blit(glow_surf, (self.x - 4, self.y - 4))
        
        # Main paddle with gradient
        for i in range(self.WIDTH):
            progress = i / self.WIDTH
            gradient_color = tuple(int(color[j] * (0.7 + 0.3 * progress)) for j in range(3))
            pygame.draw.rect(win, gradient_color, (self.x + i, self.y, 1, current_height))
        
        # Border highlight
        pygame.draw.rect(win, color, (self.x, self.y, self.WIDTH, current_height), 2, border_radius=4)
    
    def move(self, up=True):
        """
        Di chuyển vợt
        
        Args:
            up: True = lên, False = xuống
        """
        vel = self.VEL * self.speed_modifier
        if up:
            self.y -= vel
        else:
            self.y += vel
    
    def reset(self):
        """Reset vợt về vị trí ban đầu"""
        self.x = self.original_x
        self.y = self.original_y
        self.height_modifier = 1.0
        self.speed_modifier = 1.0
    
    def get_current_height(self):
        """Lấy chiều cao hiện tại (có tính modifier)"""
        return int(self.HEIGHT * self.height_modifier)
    
    def apply_height_modifier(self, modifier):
        """Áp dụng height modifier từ power-ups"""
        self.height_modifier = modifier
    
    def apply_speed_modifier(self, modifier):
        """Áp dụng speed modifier từ power-ups"""
        self.speed_modifier = modifier
