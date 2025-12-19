"""
Power-ups System - TV2 (Dũng)
Hệ thống vật phẩm trong game
"""
import pygame
import random


class PowerUpType:
    """Các loại power-up"""
    PADDLE_SIZE_UP = "paddle_size_up"
    PADDLE_SIZE_DOWN = "paddle_size_down"
    BALL_SPEED_UP = "ball_speed_up"
    BALL_SPEED_DOWN = "ball_speed_down"
    PADDLE_SPEED_UP = "paddle_speed_up"


class PowerUp:
    """Một power-up instance"""
    
    WIDTH = 30
    HEIGHT = 30
    LIFETIME = 5000  # 5 seconds
    
    COLORS = {
        PowerUpType.PADDLE_SIZE_UP: (0, 255, 0),
        PowerUpType.PADDLE_SIZE_DOWN: (255, 0, 0),
        PowerUpType.BALL_SPEED_UP: (255, 255, 0),
        PowerUpType.BALL_SPEED_DOWN: (0, 255, 255),
        PowerUpType.PADDLE_SPEED_UP: (255, 165, 0),
    }
    
    def __init__(self, x, y, powerup_type):
        self.x = x
        self.y = y
        self.type = powerup_type
        self.spawn_time = pygame.time.get_ticks()
        self.active = True
    
    def is_expired(self):
        """Kiểm tra đã hết hạn chưa"""
        return pygame.time.get_ticks() - self.spawn_time > self.LIFETIME
    
    def draw(self, win):
        """Vẽ power-up"""
        if not self.active:
            return
        
        color = self.COLORS.get(self.type, (255, 255, 255))
        
        # Outer rectangle
        pygame.draw.rect(win, color, (self.x, self.y, self.WIDTH, self.HEIGHT))
        
        # Inner rectangle (border effect)
        pygame.draw.rect(win, (0, 0, 0), 
                        (self.x + 3, self.y + 3, self.WIDTH - 6, self.HEIGHT - 6))
        
        # Center dot
        center_x = self.x + self.WIDTH // 2
        center_y = self.y + self.HEIGHT // 2
        pygame.draw.circle(win, color, (center_x, center_y), 5)
    
    def check_collision(self, ball_x, ball_y, ball_radius):
        """Kiểm tra va chạm với bóng"""
        if not self.active:
            return False
        
        return (self.x < ball_x + ball_radius and
                self.x + self.WIDTH > ball_x - ball_radius and
                self.y < ball_y + ball_radius and
                self.y + self.HEIGHT > ball_y - ball_radius)


class PowerUpManager:
    """Quản lý power-ups"""
    
    def __init__(self, window_width, window_height):
        """
        Khởi tạo manager
        
        Args:
            window_width: Chiều rộng window
            window_height: Chiều cao window
        """
        self.window_width = window_width
        self.window_height = window_height
        self.active_powerups = []
        self.hit_count = 0
        self.spawn_threshold = 5  # Spawn sau N hits
        self.max_powerups = 1
        self.active_effects = {}  # {effect_id: {'type': ..., 'expires': ...}}
    
    def update(self, hits):
        """
        Update power-up system
        
        Args:
            hits: Tổng số hits hiện tại
        """
        # Remove expired power-ups
        self.active_powerups = [p for p in self.active_powerups 
                               if not p.is_expired()]
        
        # Spawn new power-up?
        if hits > 0 and hits != self.hit_count:
            self.hit_count = hits
            
            if hits % self.spawn_threshold == 0:
                if len(self.active_powerups) < self.max_powerups:
                    self.spawn_random_powerup()
        
        # Remove expired effects
        current_time = pygame.time.get_ticks()
        expired = [k for k, v in self.active_effects.items() 
                  if current_time > v['expires']]
        for effect_id in expired:
            del self.active_effects[effect_id]
    
    def spawn_random_powerup(self):
        """Spawn power-up ngẫu nhiên"""
        # Random position (tránh edges)
        x = random.randint(100, self.window_width - 100)
        y = random.randint(100, self.window_height - 100)
        
        # Random type
        types = [
            PowerUpType.PADDLE_SIZE_UP,
            PowerUpType.PADDLE_SIZE_DOWN,
            PowerUpType.BALL_SPEED_UP,
            PowerUpType.BALL_SPEED_DOWN,
            PowerUpType.PADDLE_SPEED_UP,
        ]
        powerup_type = random.choice(types)
        
        powerup = PowerUp(x, y, powerup_type)
        self.active_powerups.append(powerup)
        
        print(f"✨ Power-up spawned: {powerup_type} at ({x}, {y})")
    
    def check_collisions(self, ball_x, ball_y, ball_radius):
        """
        Kiểm tra va chạm với bóng
        
        Args:
            ball_x, ball_y: Vị trí bóng
            ball_radius: Bán kính bóng
        
        Returns:
            PowerUp hoặc None
        """
        for powerup in self.active_powerups[:]:
            if powerup.check_collision(ball_x, ball_y, ball_radius):
                powerup.active = False
                self.active_powerups.remove(powerup)
                self._activate_effect(powerup.type)
                return powerup
        return None
    
    def _activate_effect(self, powerup_type, duration=5000):
        """Kích hoạt effect"""
        effect_id = f"{powerup_type}_{pygame.time.get_ticks()}"
        self.active_effects[effect_id] = {
            'type': powerup_type,
            'expires': pygame.time.get_ticks() + duration
        }
        print(f"⚡ Effect activated: {powerup_type} for {duration/1000}s")
    
    def get_modifiers(self):
        """
        Lấy modifiers hiện tại từ active effects
        
        Returns:
            dict: {'paddle_height': float, 'paddle_speed': float, 'ball_speed': float}
        """
        modifiers = {
            'paddle_height': 1.0,
            'paddle_speed': 1.0,
            'ball_speed': 1.0
        }
        
        for effect_id, effect in self.active_effects.items():
            effect_type = effect['type']
            
            if effect_type == PowerUpType.PADDLE_SIZE_UP:
                modifiers['paddle_height'] *= 1.5
            elif effect_type == PowerUpType.PADDLE_SIZE_DOWN:
                modifiers['paddle_height'] *= 0.7
            elif effect_type == PowerUpType.PADDLE_SPEED_UP:
                modifiers['paddle_speed'] *= 1.5
            elif effect_type == PowerUpType.BALL_SPEED_UP:
                modifiers['ball_speed'] *= 1.3
            elif effect_type == PowerUpType.BALL_SPEED_DOWN:
                modifiers['ball_speed'] *= 0.8
        
        return modifiers
    
    def draw(self, win):
        """Vẽ tất cả power-ups"""
        for powerup in self.active_powerups:
            powerup.draw(win)
    
    def reset(self):
        """Reset hệ thống"""
        self.active_powerups.clear()
        self.active_effects.clear()
        self.hit_count = 0
