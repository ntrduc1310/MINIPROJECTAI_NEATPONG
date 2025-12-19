"""
Ball Class - TV2 (Dũng)
Xử lý di chuyển và vật lý của bóng
"""
import pygame
import math
import random


class Ball:
    """Ball với physics đầy đủ"""
    
    MAX_VEL = 5
    RADIUS = 7
    
    def __init__(self, x, y):
        """
        Khởi tạo bóng
        
        Args:
            x: Vị trí X
            y: Vị trí Y
        """
        self.x = self.original_x = x
        self.y = self.original_y = y
        
        # Random angle và direction
        angle = self._get_random_angle(-30, 30, [0])
        pos = 1 if random.random() < 0.5 else -1
        
        self.x_vel = pos * abs(math.cos(angle) * self.MAX_VEL)
        self.y_vel = math.sin(angle) * self.MAX_VEL
        
        # Speed modifier cho power-ups
        self.speed_modifier = 1.0
    
    def _get_random_angle(self, min_angle, max_angle, excluded):
        """Lấy góc random, tránh các góc excluded"""
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))
        return angle
    
    def draw(self, win, color=(255, 255, 255)):
        """
        Vẽ bóng
        
        Args:
            win: Pygame window
            color: Màu bóng (RGB tuple)
        """
        pygame.draw.circle(win, color, (self.x, self.y), self.RADIUS)
    
    def move(self):
        """Di chuyển bóng theo vận tốc"""
        self.x += self.x_vel * self.speed_modifier
        self.y += self.y_vel * self.speed_modifier
    
    def reset(self):
        """Reset bóng về vị trí ban đầu"""
        self.x = self.original_x
        self.y = self.original_y
        
        angle = self._get_random_angle(-30, 30, [0])
        x_vel = abs(math.cos(angle) * self.MAX_VEL)
        y_vel = math.sin(angle) * self.MAX_VEL
        
        self.y_vel = y_vel
        self.x_vel *= -1
        self.speed_modifier = 1.0
    
    def apply_speed_modifier(self, modifier):
        """
        Áp dụng speed modifier từ power-ups
        
        Args:
            modifier: Hệ số tốc độ (1.0 = normal, >1.0 = fast, <1.0 = slow)
        """
        self.speed_modifier = modifier
