"""
Main Menu System - TV4 (Bảo)
Professional UI with gradients, animations & effects
"""
import pygame
import sys
import math
import random


class MenuButton:
    """Modern button with gradient and animations"""
    
    def __init__(self, x, y, width, height, text, font, 
                 color=(100, 100, 100), hover_color=(150, 150, 150),
                 text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.hover_progress = 0
        self.scale = 1.0
        self.glow_alpha = 0
    
    def update(self):
        """Update animation states"""
        # Smooth hover transition
        if self.is_hovered:
            self.hover_progress = min(1.0, self.hover_progress + 0.1)
            self.scale = 1.0 + (0.05 * self.hover_progress)
            self.glow_alpha = min(100, self.glow_alpha + 10)
        else:
            self.hover_progress = max(0.0, self.hover_progress - 0.1)
            self.scale = 1.0 + (0.05 * self.hover_progress)
            self.glow_alpha = max(0, self.glow_alpha - 10)
    
    def draw(self, win):
        """Draw button with gradient and effects"""
        self.update()
        
        # Calculate scaled rect
        scaled_width = int(self.rect.width * self.scale)
        scaled_height = int(self.rect.height * self.scale)
        scaled_rect = pygame.Rect(
            self.rect.centerx - scaled_width // 2,
            self.rect.centery - scaled_height // 2,
            scaled_width,
            scaled_height
        )
        
        # Glow effect
        if self.glow_alpha > 0:
            glow_surf = pygame.Surface((scaled_width + 20, scaled_height + 20), pygame.SRCALPHA)
            glow_color = (*self.hover_color, self.glow_alpha)
            pygame.draw.rect(glow_surf, glow_color, 
                           glow_surf.get_rect(), border_radius=15)
            win.blit(glow_surf, (scaled_rect.x - 10, scaled_rect.y - 10))
        
        # Interpolate color
        t = self.hover_progress
        current_color = tuple(
            int(self.color[i] + (self.hover_color[i] - self.color[i]) * t)
            for i in range(3)
        )
        
        # Button background with gradient
        self._draw_gradient(win, scaled_rect, current_color)
        
        # Border
        border_color = tuple(min(255, c + 50) for c in current_color)
        pygame.draw.rect(win, border_color, scaled_rect, 3, border_radius=12)
        
        # Text with shadow
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=scaled_rect.center)
        
        # Shadow
        shadow_surface = self.font.render(self.text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(scaled_rect.centerx + 2, scaled_rect.centery + 2))
        win.blit(shadow_surface, shadow_rect)
        
        # Text
        win.blit(text_surface, text_rect)
    
    def _draw_gradient(self, win, rect, color):
        """Draw vertical gradient"""
        for i in range(rect.height):
            progress = i / rect.height
            gradient_color = tuple(int(color[j] * (1 - progress * 0.3)) for j in range(3))
            pygame.draw.line(win, gradient_color,
                           (rect.left, rect.top + i),
                           (rect.right, rect.top + i))
        pygame.draw.rect(win, color, rect, border_radius=12)
    
    def handle_event(self, event):
        """
        Xử lý sự kiện
        
        Args:
            event: Pygame event
        
        Returns:
            bool: True nếu button được click
        """
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Ignore mousewheel clicks (button 4 and 5)
            if event.button in (4, 5):
                return False
            # Only handle left click (button 1)
            if event.button == 1 and self.is_hovered:
                return True
        
        return False


class MainMenu:
    """Professional menu with particles and animations"""
    
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.running = True
        self.selected_option = None
        
        # Initialize pygame
        pygame.init()
        self.win = pygame.display.set_mode((width, height))
        pygame.display.set_caption("NEAT Pong AI - Neural Evolution")
        
        # Fonts
        self.title_font = pygame.font.Font(None, 90)
        self.button_font = pygame.font.Font(None, 42)
        self.subtitle_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)
        
        # Buttons
        self.buttons = self._create_buttons()
        
        # Particles
        self.particles = []
        self.spawn_particles()
        
        # Animation
        self.time = 0
        self.title_float = 0
        
        # Clock
        self.clock = pygame.time.Clock()
    
    def spawn_particles(self):
        """Create background particles"""
        for _ in range(50):
            self.particles.append({
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'speed': random.uniform(0.5, 2),
                'size': random.randint(1, 3),
                'alpha': random.randint(50, 150)
            })
    
    def update_particles(self):
        """Update particle positions"""
        for p in self.particles:
            p['y'] += p['speed']
            if p['y'] > self.height:
                p['y'] = 0
                p['x'] = random.randint(0, self.width)
    
    def _create_buttons(self):
        """Create modern buttons"""
        button_width = 350
        button_height = 65
        button_x = self.width // 2 - button_width // 2
        start_y = 220
        spacing = 85
        
        buttons = {
            'train': MenuButton(
                button_x, start_y,
                button_width, button_height,
                ">> Train AI Network",
                self.button_font,
                color=(30, 120, 30),
                hover_color=(40, 180, 40)
            ),
            'play_easy': MenuButton(
                button_x, start_y + spacing,
                button_width, button_height,
                "[1] Easy AI",
                self.button_font,
                color=(40, 90, 200),
                hover_color=(60, 120, 255)
            ),
            'play_medium': MenuButton(
                button_x, start_y + spacing * 2,
                button_width, button_height,
                "[2] Medium AI",
                self.button_font,
                color=(180, 100, 30),
                hover_color=(220, 140, 50)
            ),
            'play_hard': MenuButton(
                button_x, start_y + spacing * 3,
                button_width, button_height,
                "[3] Hard AI",
                self.button_font,
                color=(180, 30, 30),
                hover_color=(240, 50, 50)
            ),
            'quit': MenuButton(
                button_x, start_y + spacing * 4,
                button_width, button_height,
                "[X] Quit",
                self.button_font,
                color=(80, 80, 80),
                hover_color=(120, 120, 120)
            )
        }
        
        return buttons
    
    def run(self):
        """
        Chạy menu loop
        
        Returns:
            str: Selected option ('train', 'play_easy', 'play_medium', 'play_hard', 'quit')
        """
        while self.running:
            self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.selected_option = 'quit'
                    self.running = False
                    continue
                
                # Ignore mousewheel events
                if event.type == pygame.MOUSEWHEEL:
                    continue
                
                # Check button clicks
                for option, button in self.buttons.items():
                    if button.handle_event(event):
                        self.selected_option = option
                        self.running = False
                        break
            
            self._draw()
        
        return self.selected_option
    
    def _draw(self):
        """Draw menu with effects"""
        self.time += 1
        self.title_float = math.sin(self.time * 0.05) * 5
        
        # Background gradient
        for y in range(self.height):
            progress = y / self.height
            color = (
                int(10 + 20 * progress),
                int(15 + 25 * progress),
                int(35 + 40 * progress)
            )
            pygame.draw.line(self.win, color, (0, y), (self.width, y))
        
        # Particles
        self.update_particles()
        for p in self.particles:
            s = pygame.Surface((p['size'] * 2, p['size'] * 2), pygame.SRCALPHA)
            color = (100, 200, 255, p['alpha'])
            pygame.draw.circle(s, color, (p['size'], p['size']), p['size'])
            self.win.blit(s, (int(p['x']), int(p['y'])))
        
        # Title with glow
        title_y = 70 + self.title_float
        
        # Glow effect
        for offset in range(5, 0, -1):
            glow_alpha = 30 - offset * 5
            glow_surf = self.title_font.render("🤖 NEAT PONG", True, (0, 200, 255))
            glow_surf.set_alpha(glow_alpha)
            glow_rect = glow_surf.get_rect(center=(self.width // 2, title_y))
            self.win.blit(glow_surf, glow_rect.move(offset, offset))
        
        # Main title
        title = self.title_font.render("NEAT PONG AI", True, (0, 255, 255))
        title_rect = title.get_rect(center=(self.width // 2, title_y))
        self.win.blit(title, title_rect)
        
        # Subtitle with better spacing
        subtitle = self.subtitle_font.render(
            "Neural Evolution AI Gaming",
            True, (150, 220, 255)
        )
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, title_y + 60))
        self.win.blit(subtitle, subtitle_rect)
        
        # Decorative line
        line_y = title_y + 95
        pygame.draw.line(self.win, (0, 200, 255), 
                        (self.width // 2 - 150, line_y),
                        (self.width // 2 + 150, line_y), 2)
        
        # Buttons
        for button in self.buttons.values():
            button.draw(self.win)
        
        # Footer info
        footer_y = self.height - 50
        team_text = self.small_font.render(
            "Team: TV1 (AI) - TV2 (Physics) - TV3 (Analytics) - TV4 (UI)",
            True, (100, 150, 180)
        )
        team_rect = team_text.get_rect(center=(self.width // 2, footer_y))
        self.win.blit(team_text, team_rect)
        
        tech_text = self.small_font.render(
            "Powered by NEAT-Python & Pygame",
            True, (80, 120, 150)
        )
        tech_rect = tech_text.get_rect(center=(self.width // 2, footer_y + 22))
        self.win.blit(tech_text, tech_rect)
        
        pygame.display.update()
    
    def close(self):
        """Đóng menu"""
        pygame.quit()


def show_menu(width=800, height=600):
    """
    Hiển thị menu và trả về lựa chọn
    
    Args:
        width, height: Kích thước window
    
    Returns:
        str: Selected option
    """
    menu = MainMenu(width, height)
    choice = menu.run()
    menu.close()
    return choice
