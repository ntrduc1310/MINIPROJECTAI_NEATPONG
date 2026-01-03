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
        self.fullscreen = False
        
        # Theme system
        self.dark_mode = True
        self.themes = {
            'dark': {
                'bg_start': (10, 15, 35),
                'bg_end': (30, 40, 75),
                'particles': (100, 200, 255),
                'title': (0, 255, 255),
                'title_glow': (0, 200, 255),
                'subtitle': (150, 220, 255),
                'divider': (0, 200, 255),
                'text': (100, 150, 180)
            },
            'light': {
                'bg_start': (240, 245, 255),
                'bg_end': (200, 220, 245),
                'particles': (100, 150, 255),
                'title': (20, 100, 200),
                'title_glow': (50, 130, 230),
                'subtitle': (60, 120, 200),
                'divider': (100, 150, 255),
                'text': (80, 100, 130)
            }
        }
        
        # Initialize pygame
        pygame.init()
        
        # Get desktop resolution for fullscreen
        display_info = pygame.display.Info()
        self.desktop_width = display_info.current_w
        self.desktop_height = display_info.current_h
        
        if self.fullscreen:
            self.win = pygame.display.set_mode((self.desktop_width, self.desktop_height), pygame.FULLSCREEN)
            self.width = self.desktop_width
            self.height = self.desktop_height
        else:
            self.win = pygame.display.set_mode((width, height))
        
        pygame.display.set_caption("NEAT Pong - AI Training System")
        
        # Fonts
        self.title_font = pygame.font.Font(None, 90)
        self.button_font = pygame.font.Font(None, 42)
        self.subtitle_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)
        
        # Theme toggle button (top right)
        theme_text = "Dark Mode" if self.dark_mode else "Light Mode"
        self.theme_button = MenuButton(
            self.width - 160, 20,
            140, 45,
            theme_text,
            pygame.font.Font(None, 24),
            color=(60, 60, 80),
            hover_color=(90, 90, 120)
        )
        
        # Fullscreen toggle button (top right, below theme)
        fs_text = "Windowed" if self.fullscreen else "Fullscreen"
        self.fullscreen_button = MenuButton(
            self.width - 160, 75,
            140, 45,
            fs_text,
            pygame.font.Font(None, 24),
            color=(60, 80, 60),
            hover_color=(90, 120, 90)
        )
        
        # Buttons
        self.buttons = self._create_buttons()
        
        # Particles
        self.particles = []
        self.spawn_particles()
        
        # Scroll support
        self.scroll_offset = 0
        self.max_scroll = 0
        self.scroll_speed = 30
        
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
    
    def get_theme(self):
        """Get current theme colors"""
        return self.themes['dark'] if self.dark_mode else self.themes['light']
    
    def calculate_max_scroll(self):
        """Calculate maximum scroll based on content height"""
        scale = min(self.width / 800, self.height / 600)
        # Content area (buttons + spacing)
        content_height = int(220 * scale) + (5 * int(85 * scale)) + int(65 * scale)
        # Visible area (excluding header and footer)
        visible_height = self.height - int(200 * scale) - int(120 * scale)
        
        self.max_scroll = max(0, content_height - visible_height)
        return self.max_scroll
    
    def toggle_theme(self):
        """Toggle between dark and light theme"""
        self.dark_mode = not self.dark_mode
        self.theme_button.text = "Dark Mode" if self.dark_mode else "Light Mode"
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        self.fullscreen = not self.fullscreen
        
        if self.fullscreen:
            self.win = pygame.display.set_mode((self.desktop_width, self.desktop_height), pygame.FULLSCREEN)
            self.width = self.desktop_width
            self.height = self.desktop_height
        else:
            self.width = 800
            self.height = 600
            self.win = pygame.display.set_mode((self.width, self.height))
        
        # Recreate all UI elements with new scale
        self._recreate_ui_elements()
        self.fullscreen_button.text = "Windowed" if self.fullscreen else "Fullscreen"
        
        # Reset scroll
        self.scroll_offset = 0
        self.calculate_max_scroll()
    
    def _recreate_ui_elements(self):
        """Recreate UI elements with proper scaling"""
        # Calculate scale factor
        scale = min(self.width / 800, self.height / 600)
        
        # Update fonts with scaling
        self.title_font = pygame.font.Font(None, int(90 * scale))
        self.button_font = pygame.font.Font(None, int(42 * scale))
        self.subtitle_font = pygame.font.Font(None, int(28 * scale))
        self.small_font = pygame.font.Font(None, int(22 * scale))
        
        # Update theme button
        theme_text = "Dark Mode" if self.dark_mode else "Light Mode"
        button_font_small = pygame.font.Font(None, int(24 * scale))
        self.theme_button = MenuButton(
            self.width - int(160 * scale), int(20 * scale),
            int(140 * scale), int(45 * scale),
            theme_text,
            button_font_small,
            color=(60, 60, 80),
            hover_color=(90, 90, 120)
        )
        
        # Update fullscreen button
        fs_text = "Windowed" if self.fullscreen else "Fullscreen"
        self.fullscreen_button = MenuButton(
            self.width - int(160 * scale), int(75 * scale),
            int(140 * scale), int(45 * scale),
            fs_text,
            button_font_small,
            color=(60, 80, 60),
            hover_color=(90, 120, 90)
        )
        
        # Recreate main buttons
        self.buttons = self._create_buttons()
    
    def update_particles(self):
        """Update particle positions"""
        for p in self.particles:
            p['y'] += p['speed']
            if p['y'] > self.height:
                p['y'] = 0
                p['x'] = random.randint(0, self.width)
    
    def _create_buttons(self):
        """Create modern buttons with scaling"""
        # Calculate scale factor for responsive design
        scale = min(self.width / 800, self.height / 600)
        
        button_width = int(350 * scale)
        button_height = int(65 * scale)
        button_x = self.width // 2 - button_width // 2
        start_y = int(220 * scale)
        spacing = int(85 * scale)
        
        # Calculate max scroll
        self.calculate_max_scroll()
        
        buttons = {
            'train': MenuButton(
                button_x, start_y,
                button_width, button_height,
                "[T] Train AI Network",
                self.button_font,
                color=(30, 120, 30),
                hover_color=(40, 180, 40)
            ),
            'play_easy': MenuButton(
                button_x, start_y + spacing,
                button_width, button_height,
                "[E] Easy AI",
                self.button_font,
                color=(40, 90, 200),
                hover_color=(60, 120, 255)
            ),
            'play_medium': MenuButton(
                button_x, start_y + spacing * 2,
                button_width, button_height,
                "[M] Medium AI",
                self.button_font,
                color=(180, 100, 30),
                hover_color=(220, 140, 50)
            ),
            'play_hard': MenuButton(
                button_x, start_y + spacing * 3,
                button_width, button_height,
                "[H] Hard AI",
                self.button_font,
                color=(180, 30, 30),
                hover_color=(240, 50, 50)
            ),
            'quit': MenuButton(
                button_x, start_y + spacing * 4,
                button_width, button_height,
                "[Q] Quit",
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
            
            # Update mouse position for all buttons
            mouse_pos = pygame.mouse.get_pos()
            self.theme_button.is_hovered = self.theme_button.rect.collidepoint(mouse_pos)
            self.fullscreen_button.is_hovered = self.fullscreen_button.rect.collidepoint(mouse_pos)
            
            # Check button hover with scroll offset
            for button in self.buttons.values():
                # Adjust mouse position for scroll
                adjusted_mouse = (mouse_pos[0], mouse_pos[1] + self.scroll_offset)
                button.is_hovered = button.rect.collidepoint(adjusted_mouse)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.selected_option = 'quit'
                    self.running = False
                    continue
                
                # F11 for fullscreen toggle
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.toggle_fullscreen()
                        continue
                    elif event.key == pygame.K_ESCAPE and self.fullscreen:
                        self.toggle_fullscreen()
                        continue
                    # Keyboard shortcuts
                    elif event.key == pygame.K_t:
                        self.selected_option = 'train'
                        self.running = False
                        break
                    elif event.key == pygame.K_e:
                        self.selected_option = 'play_easy'
                        self.running = False
                        break
                    elif event.key == pygame.K_m:
                        self.selected_option = 'play_medium'
                        self.running = False
                        break
                    elif event.key == pygame.K_h:
                        self.selected_option = 'play_hard'
                        self.running = False
                        break
                    elif event.key == pygame.K_q:
                        self.selected_option = 'quit'
                        self.running = False
                        break
                
                # Mouse wheel for scrolling
                if event.type == pygame.MOUSEWHEEL:
                    # Scroll up (positive) or down (negative)
                    self.scroll_offset -= event.y * self.scroll_speed
                    self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
                
                # Check theme button first
                if self.theme_button.handle_event(event):
                    self.toggle_theme()
                    continue
                
                # Check fullscreen button
                if self.fullscreen_button.handle_event(event):
                    self.toggle_fullscreen()
                    continue
                
                # Check other buttons
                button_clicked = False
                for option, button in self.buttons.items():
                    if button.handle_event(event):
                        self.selected_option = option
                        self.running = False
                        button_clicked = True
                        break
                
                if button_clicked:
                    break
            
            self._draw()
        
        return self.selected_option
    
    def _draw(self):
        """Draw menu with effects"""
        self.time += 1
        self.title_float = math.sin(self.time * 0.05) * 5
        theme = self.get_theme()
        scale = min(self.width / 800, self.height / 600)
        
        # Background gradient with theme
        for y in range(self.height):
            progress = y / self.height
            color = tuple(
                int(theme['bg_start'][i] + (theme['bg_end'][i] - theme['bg_start'][i]) * progress)
                for i in range(3)
            )
            pygame.draw.line(self.win, color, (0, y), (self.width, y))
        
        # Particles with theme
        self.update_particles()
        for p in self.particles:
            s = pygame.Surface((p['size'] * 2, p['size'] * 2), pygame.SRCALPHA)
            color = (*theme['particles'], p['alpha'])
            pygame.draw.circle(s, color, (p['size'], p['size']), p['size'])
            self.win.blit(s, (int(p['x']), int(p['y'])))
        
        # Title with glow
        title_y = int(70 * scale) + self.title_float
        
        # Glow effect
        for offset in range(5, 0, -1):
            glow_alpha = 30 - offset * 5
            glow_surf = self.title_font.render("NEAT PONG", True, theme['title_glow'])
            glow_surf.set_alpha(glow_alpha)
            glow_rect = glow_surf.get_rect(center=(self.width // 2, title_y))
            self.win.blit(glow_surf, glow_rect.move(offset, offset))
        
        # Main title
        title = self.title_font.render("NEAT PONG", True, theme['title'])
        title_rect = title.get_rect(center=(self.width // 2, title_y))
        self.win.blit(title, title_rect)
        
        # Subtitle with better spacing
        subtitle = self.subtitle_font.render(
            "AI Training System",
            True, theme['subtitle']
        )
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, title_y + int(60 * scale)))
        self.win.blit(subtitle, subtitle_rect)
        
        # Decorative line
        line_y = title_y + int(95 * scale)
        line_width = int(150 * scale)
        pygame.draw.line(self.win, theme['divider'], 
                        (self.width // 2 - line_width, line_y),
                        (self.width // 2 + line_width, line_y), int(2 * scale))
        
        # Create scrollable content area
        content_y = int(200 * scale)
        content_height = self.height - int(320 * scale)
        
        # Save original button positions and apply scroll offset
        for button in self.buttons.values():
            # Temporarily adjust Y position for scroll
            original_y = button.rect.y
            button.rect.y = original_y - self.scroll_offset
            
            # Only draw if visible
            if button.rect.y + button.rect.height > content_y and button.rect.y < content_y + content_height:
                button.draw(self.win)
            
            # Restore original position
            button.rect.y = original_y
        
        # Theme toggle button (draw last so it's on top)
        self.theme_button.draw(self.win)
        
        # Fullscreen toggle button
        self.fullscreen_button.draw(self.win)
        
        # Draw scrollbar if needed
        if self.max_scroll > 0:
            self._draw_scrollbar(theme, scale)
        
        # Keyboard shortcuts hint (bottom left)
        hint_font = pygame.font.Font(None, int(20 * scale))
        hint_y = self.height - int(85 * scale)
        hint_text = hint_font.render("Press F11 for Fullscreen | ESC to exit fullscreen", True, theme['text'])
        self.win.blit(hint_text, (int(20 * scale), hint_y))
        
        # Footer info
        footer_y = self.height - int(50 * scale)
        team_text = self.small_font.render(
            "Team: TV1 (AI) - TV2 (Physics) - TV3 (Engine & Analytics) - TV4 (UI)",
            True, theme['text']
        )
        team_rect = team_text.get_rect(center=(self.width // 2, footer_y))
        self.win.blit(team_text, team_rect)
        
        tech_text = self.small_font.render(
            "Powered by NEAT-Python & Pygame",
            True, theme['text']
        )
        tech_rect = tech_text.get_rect(center=(self.width // 2, footer_y + int(22 * scale)))
        self.win.blit(tech_text, tech_rect)
        
        pygame.display.update()
    
    def _draw_scrollbar(self, theme, scale):
        """Draw scrollbar on the right side"""
        if self.max_scroll <= 0:
            return
        
        scrollbar_width = int(8 * scale)
        scrollbar_x = self.width - int(15 * scale)
        scrollbar_height = self.height - int(320 * scale)
        scrollbar_y = int(200 * scale)
        
        # Background track
        track_surf = pygame.Surface((scrollbar_width, scrollbar_height), pygame.SRCALPHA)
        pygame.draw.rect(track_surf, (*theme['text'], 30), track_surf.get_rect(), border_radius=int(4 * scale))
        self.win.blit(track_surf, (scrollbar_x, scrollbar_y))
        
        # Calculate thumb size and position
        content_ratio = scrollbar_height / (scrollbar_height + self.max_scroll)
        thumb_height = max(int(30 * scale), int(scrollbar_height * content_ratio))
        
        scroll_ratio = self.scroll_offset / self.max_scroll if self.max_scroll > 0 else 0
        thumb_y = scrollbar_y + int((scrollbar_height - thumb_height) * scroll_ratio)
        
        # Thumb
        thumb_surf = pygame.Surface((scrollbar_width, thumb_height), pygame.SRCALPHA)
        pygame.draw.rect(thumb_surf, (*theme['divider'], 180), thumb_surf.get_rect(), border_radius=int(4 * scale))
        self.win.blit(thumb_surf, (scrollbar_x, thumb_y))
    
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
