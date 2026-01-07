"""
Visual Effects & Asset Management - TV4 (Bảo)
Quản lý assets và hiệu ứng
"""
import pygame
import os


class AssetManager:
    """Quản lý fonts và assets"""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Khởi tạo manager"""
        if self._initialized:
            return
        
        self.fonts = {}
        self.assets_dir = "assets"
        self.fonts_dir = os.path.join(self.assets_dir, "fonts")
        self._initialized = True
        
        # Ensure directories exist
        os.makedirs(self.fonts_dir, exist_ok=True)
    
    def get_font(self, name, size):
        """
        Lấy font (cache)
        
        Args:
            name: Font name (None for default)
            size: Font size
        
        Returns:
            pygame.font.Font
        """
        key = f"{name}_{size}"
        
        if key not in self.fonts:
            try:
                if name:
                    font_path = os.path.join(self.fonts_dir, name)
                    if os.path.exists(font_path):
                        self.fonts[key] = pygame.font.Font(font_path, size)
                    else:
                        print(f"Warning: Font not found: {font_path}, using default")
                        self.fonts[key] = pygame.font.Font(None, size)
                else:
                    self.fonts[key] = pygame.font.Font(None, size)
            except Exception as e:
                print(f"Error loading font {name}: {e}")
                self.fonts[key] = pygame.font.Font(None, size)
        
        return self.fonts[key]
    
    def list_available_fonts(self):
        """Liệt kê các fonts có sẵn"""
        if not os.path.exists(self.fonts_dir):
            return []
        
        fonts = [f for f in os.listdir(self.fonts_dir) 
                if f.endswith('.ttf') or f.endswith('.otf')]
        return fonts


class VisualEffects:
    """Hiệu ứng visual cho game với trail effects"""
    
    def __init__(self):
        """Khởi tạo effects"""
        self.particles = []
        self.screen_shake = 0
        self.flash_alpha = 0
        self.ball_trail = []  # Trail effect cho ball
        self.max_trail_length = 15
    
    def add_ball_position(self, x, y):
        """Thêm vị trí ball vào trail"""
        self.ball_trail.append({'x': x, 'y': y, 'life': 15})
        if len(self.ball_trail) > self.max_trail_length:
            self.ball_trail.pop(0)
    
    def add_hit_effect(self, x, y, color=(255, 255, 255)):
        """
        Thêm effect khi đánh bóng - sử dụng màu tối cho nền sáng
        
        Args:
            x, y: Vị trí
            color: Màu particles
        """
        import random
        
        # Tạo particles với màu tối
        particle_color = (80, 50, 30)  # Màu nâu tối cho nền vàng
        
        for _ in range(15):
            particle = {
                'x': x,
                'y': y,
                'vx': random.uniform(-8, 8),
                'vy': random.uniform(-8, 8),
                'lifetime': 40,
                'color': particle_color,
                'size': random.randint(3, 6)
            }
            self.particles.append(particle)
        
        # Screen shake
        self.screen_shake = 8
    
    def add_score_effect(self, x, y):
        """
        Effect khi ghi điểm
        
        Args:
            x, y: Vị trí
        """
        self.flash_alpha = 70
        # Vàng sáng cho effect ghi điểm
        self.add_hit_effect(x, y, color=(255, 200, 0))
    
    def update(self):
        """Update tất cả effects"""
        # Update particles
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.3  # Gravity
            particle['vx'] *= 0.98  # Air resistance
            particle['lifetime'] -= 1
            
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
        
        # Update trail
        for trail in self.ball_trail[:]:
            trail['life'] -= 1
            if trail['life'] <= 0:
                self.ball_trail.remove(trail)
        
        # Update screen shake
        if self.screen_shake > 0:
            self.screen_shake -= 1
        
        # Update flash
        if self.flash_alpha > 0:
            self.flash_alpha -= 3
    
    def draw(self, win):
        """
        Vẽ effects và trail
        
        Args:
            win: Pygame window
        """
        # Draw ball trail
        for i, trail in enumerate(self.ball_trail):
            alpha = int((trail['life'] / 15) * 120)
            size = max(3, int(7 * (trail['life'] / 15)))
            color = (100, 70, 50, alpha)  # Nâu tối với alpha
            
            surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (size, size), size)
            win.blit(surf, (trail['x'] - size, trail['y'] - size))
        
        # Draw particles
        for particle in self.particles:
            alpha = int((particle['lifetime'] / 40) * 200)
            color = (*particle['color'], alpha)
            
            # Create surface with alpha
            surf = pygame.Surface((particle['size'] * 2, particle['size'] * 2), 
                                 pygame.SRCALPHA)
            pygame.draw.circle(surf, color, 
                             (particle['size'], particle['size']), 
                             particle['size'])
            
            win.blit(surf, (particle['x'] - particle['size'], 
                           particle['y'] - particle['size']))
        
        # Draw flash (white flash for score)
        if self.flash_alpha > 0:
            flash_surf = pygame.Surface(win.get_size(), pygame.SRCALPHA)
            flash_surf.fill((255, 255, 255, self.flash_alpha))
            win.blit(flash_surf, (0, 0))
    
    def get_shake_offset(self):
        """
        Lấy offset cho screen shake
        
        Returns:
            tuple: (x_offset, y_offset)
        """
        if self.screen_shake > 0:
            import random
            shake_amount = self.screen_shake // 2
            return (random.randint(-shake_amount, shake_amount),
                   random.randint(-shake_amount, shake_amount))
        return (0, 0)
    
    def reset(self):
        """Reset effects"""
        self.particles.clear()
        self.ball_trail.clear()
        self.screen_shake = 0
        self.flash_alpha = 0


class ScoreDisplay:
    """Professional score display with modern UI"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.score_font = pygame.font.Font(None, 80)
        self.label_font = pygame.font.Font(None, 32)
        self.hits_font = pygame.font.Font(None, 28)
        
        # Animation
        self.left_score_scale = 1.0
        self.right_score_scale = 1.0
        self.left_glow = 0
        self.right_glow = 0
    
    def draw(self, win, left_score, right_score, hits=None):
        """Draw modern score display with beautiful player badges"""
        # Update animations
        self.left_score_scale += (1.0 - self.left_score_scale) * 0.15
        self.right_score_scale += (1.0 - self.right_score_scale) * 0.15
        self.left_glow = max(0, self.left_glow - 5)
        self.right_glow = max(0, self.right_glow - 5)
        
        # Center line
        center_x = self.width // 2
        for i in range(0, self.height, 30):
            alpha = 120 if i % 60 == 0 else 60
            pygame.draw.rect(win, (80, 150, 200), 
                           (center_x - 2, i, 4, 15))
        
        # Draw Player Badge (YOU) - Left side
        self._draw_player_badge(win, self.width // 4, 35, "PLAYER", (80, 60, 40), left_score)
        
        # Draw AI Badge - Right side
        self._draw_ai_badge(win, 3 * self.width // 4, 35, "AI", (80, 60, 40), right_score)
        
        # Scores with glow
        self._draw_score(win, str(left_score), (self.width // 4, 80),
                        (100, 200, 255), self.left_score_scale, self.left_glow)
        self._draw_score(win, str(right_score), (3 * self.width // 4, 80),
                        (255, 100, 100), self.right_score_scale, self.right_glow)
        
        # Hits counter
        if hits is not None:
            bg = pygame.Surface((120, 35), pygame.SRCALPHA)
            pygame.draw.rect(bg, (30, 30, 50, 180), bg.get_rect(), border_radius=8)
            win.blit(bg, (center_x - 60, self.height - 50))
            
            hits_text = self.hits_font.render(f"HITS: {hits}", True, (255, 220, 100))
            win.blit(hits_text, hits_text.get_rect(center=(center_x, self.height - 33)))
    
    def _draw_player_badge(self, win, x, y, text, text_color, score):
        """Vẽ badge đẹp cho Player"""
        # Badge dimensions
        badge_width = 160
        badge_height = 50
        badge_x = x - badge_width // 2
        badge_y = y - badge_height // 2
        
        # Outer glow
        glow_surf = pygame.Surface((badge_width + 10, badge_height + 10), pygame.SRCALPHA)
        glow_color = (100, 200, 255, 80) if score > 0 else (100, 200, 255, 40)
        pygame.draw.rect(glow_surf, glow_color, glow_surf.get_rect(), border_radius=15)
        win.blit(glow_surf, (badge_x - 5, badge_y - 5))
        
        # Main badge background
        badge_surf = pygame.Surface((badge_width, badge_height), pygame.SRCALPHA)
        pygame.draw.rect(badge_surf, (255, 255, 255, 230), badge_surf.get_rect(), border_radius=12)
        win.blit(badge_surf, (badge_x, badge_y))
        
        # Border with gradient effect
        pygame.draw.rect(win, (100, 200, 255), 
                        (badge_x, badge_y, badge_width, badge_height), 3, border_radius=12)
        
        # Icon - Player symbol (gamepad)
        icon_x = badge_x + 15
        icon_y = badge_y + badge_height // 2
        self._draw_gamepad_icon(win, icon_x, icon_y, (100, 200, 255))
        
        # Text with shadow
        font = pygame.font.Font(None, 32)
        shadow = font.render(text, True, (50, 50, 50))
        text_surf = font.render(text, True, text_color)
        text_x = badge_x + 50
        text_y = badge_y + badge_height // 2 - text_surf.get_height() // 2
        win.blit(shadow, (text_x + 2, text_y + 2))
        win.blit(text_surf, (text_x, text_y))
    
    def _draw_ai_badge(self, win, x, y, text, text_color, score):
        """Vẽ badge đẹp cho AI"""
        # Badge dimensions
        badge_width = 140
        badge_height = 50
        badge_x = x - badge_width // 2
        badge_y = y - badge_height // 2
        
        # Outer glow
        glow_surf = pygame.Surface((badge_width + 10, badge_height + 10), pygame.SRCALPHA)
        glow_color = (255, 100, 100, 80) if score > 0 else (255, 100, 100, 40)
        pygame.draw.rect(glow_surf, glow_color, glow_surf.get_rect(), border_radius=15)
        win.blit(glow_surf, (badge_x - 5, badge_y - 5))
        
        # Main badge background
        badge_surf = pygame.Surface((badge_width, badge_height), pygame.SRCALPHA)
        pygame.draw.rect(badge_surf, (255, 255, 255, 230), badge_surf.get_rect(), border_radius=12)
        win.blit(badge_surf, (badge_x, badge_y))
        
        # Border
        pygame.draw.rect(win, (255, 100, 100), 
                        (badge_x, badge_y, badge_width, badge_height), 3, border_radius=12)
        
        # Icon - AI symbol (brain/chip)
        icon_x = badge_x + 25
        icon_y = badge_y + badge_height // 2
        self._draw_ai_icon(win, icon_x, icon_y, (255, 100, 100))
        
        # Text with shadow
        font = pygame.font.Font(None, 36)
        shadow = font.render(text, True, (50, 50, 50))
        text_surf = font.render(text, True, text_color)
        text_x = badge_x + 55
        text_y = badge_y + badge_height // 2 - text_surf.get_height() // 2
        win.blit(shadow, (text_x + 2, text_y + 2))
        win.blit(text_surf, (text_x, text_y))
    
    def _draw_gamepad_icon(self, win, x, y, color):
        """Vẽ icon gamepad đơn giản"""
        # Body
        pygame.draw.circle(win, color, (x, y), 12)
        pygame.draw.circle(win, (255, 255, 255), (x, y), 10)
        pygame.draw.circle(win, color, (x, y), 8)
        
        # D-pad
        pygame.draw.rect(win, (255, 255, 255), (x - 6, y - 2, 12, 4))
        pygame.draw.rect(win, (255, 255, 255), (x - 2, y - 6, 4, 12))
    
    def _draw_ai_icon(self, win, x, y, color):
        """Vẽ icon AI (chip/circuit)"""
        # Chip body
        pygame.draw.rect(win, color, (x - 8, y - 8, 16, 16), border_radius=2)
        pygame.draw.rect(win, (255, 255, 255), (x - 6, y - 6, 12, 12))
        
        # Circuit lines
        pygame.draw.line(win, color, (x - 4, y - 3), (x + 4, y - 3), 2)
        pygame.draw.line(win, color, (x - 4, y), (x + 4, y), 2)
        pygame.draw.line(win, color, (x - 4, y + 3), (x + 4, y + 3), 2)
        
        # Pins
        for i in [-1, 1]:
            pygame.draw.line(win, color, (x + 8 * i, y - 6), (x + 11 * i, y - 6), 2)
            pygame.draw.line(win, color, (x + 8 * i, y), (x + 11 * i, y), 2)
            pygame.draw.line(win, color, (x + 8 * i, y + 6), (x + 11 * i, y + 6), 2)
    
    def _draw_score(self, win, score, pos, color, scale, glow):
        """Draw score with effects"""
        # Glow
        if glow > 0:
            glow_surf = self.score_font.render(score, True, color)
            glow_surf.set_alpha(glow)
            for i in range(1, 4):
                win.blit(glow_surf, glow_surf.get_rect(center=(pos[0]+i, pos[1]+i)))
        
        # Shadow
        shadow = self.score_font.render(score, True, (0, 0, 0))
        win.blit(shadow, shadow.get_rect(center=(pos[0]+3, pos[1]+3)))
        
        # Main score
        surf = self.score_font.render(score, True, color)
        if scale != 1.0:
            surf = pygame.transform.scale(surf, 
                (int(surf.get_width() * scale), int(surf.get_height() * scale)))
        win.blit(surf, surf.get_rect(center=pos))
    
    def animate_score(self, left_scored=False, right_scored=False):
        """Animate scoring"""
        if left_scored:
            self.left_score_scale = 1.4
            self.left_glow = 150
        if right_scored:
            self.right_score_scale = 1.4
            self.right_glow = 150


def get_asset_manager():
    """Lấy AssetManager instance (singleton)"""
    return AssetManager()
