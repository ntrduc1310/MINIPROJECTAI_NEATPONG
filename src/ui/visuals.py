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
                        print(f"⚠️ Font not found: {font_path}, using default")
                        self.fonts[key] = pygame.font.Font(None, size)
                else:
                    self.fonts[key] = pygame.font.Font(None, size)
            except Exception as e:
                print(f"❌ Error loading font {name}: {e}")
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
    """Hiệu ứng visual cho game"""
    
    def __init__(self):
        """Khởi tạo effects"""
        self.particles = []
        self.screen_shake = 0
        self.flash_alpha = 0
    
    def add_hit_effect(self, x, y, color=(255, 255, 255)):
        """
        Thêm effect khi đánh bóng
        
        Args:
            x, y: Vị trí
            color: Màu particles
        """
        import random
        
        # Tạo particles
        for _ in range(10):
            particle = {
                'x': x,
                'y': y,
                'vx': random.uniform(-5, 5),
                'vy': random.uniform(-5, 5),
                'lifetime': 30,
                'color': color,
                'size': random.randint(2, 5)
            }
            self.particles.append(particle)
        
        # Screen shake
        self.screen_shake = 5
    
    def add_score_effect(self, x, y):
        """
        Effect khi ghi điểm
        
        Args:
            x, y: Vị trí
        """
        self.flash_alpha = 50
        self.add_hit_effect(x, y, color=(255, 255, 0))
    
    def update(self):
        """Update tất cả effects"""
        # Update particles
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.2  # Gravity
            particle['lifetime'] -= 1
            
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
        
        # Update screen shake
        if self.screen_shake > 0:
            self.screen_shake -= 1
        
        # Update flash
        if self.flash_alpha > 0:
            self.flash_alpha -= 2
    
    def draw(self, win):
        """
        Vẽ effects
        
        Args:
            win: Pygame window
        """
        # Draw particles
        for particle in self.particles:
            alpha = int((particle['lifetime'] / 30) * 255)
            color = (*particle['color'], alpha)
            
            # Create surface with alpha
            surf = pygame.Surface((particle['size'] * 2, particle['size'] * 2), 
                                 pygame.SRCALPHA)
            pygame.draw.circle(surf, color, 
                             (particle['size'], particle['size']), 
                             particle['size'])
            
            win.blit(surf, (particle['x'] - particle['size'], 
                           particle['y'] - particle['size']))
        
        # Draw flash
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
        """Draw modern score display"""
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
        
        # Player label
        player_label = self.label_font.render("< YOU", True, (100, 200, 255))
        win.blit(player_label, player_label.get_rect(center=(self.width // 4, 30)))
        
        # AI label  
        ai_label = self.label_font.render("AI >", True, (255, 100, 100))
        win.blit(ai_label, ai_label.get_rect(center=(3 * self.width // 4, 30)))
        
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
