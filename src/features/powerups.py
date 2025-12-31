"""
Power-ups System - TV2 (Dũng)
Hệ thống vật phẩm trong game - Optimized for NEAT
"""
import pygame
import random
import math  # Thêm thư viện toán để tính va chạm chuẩn hơn

class PowerUpType:
    """Các loại power-up"""
    PADDLE_SIZE_UP = "paddle_size_up"      # Icon: Dấu cộng (+)
    PADDLE_SIZE_DOWN = "paddle_size_down"  # Icon: Dấu trừ (-)
    BALL_SPEED_UP = "ball_speed_up"        # Icon: Mũi tên kép (>>)
    BALL_SPEED_DOWN = "ball_speed_down"    # Icon: Mũi tên lùi (<<)
    PADDLE_SPEED_UP = "paddle_speed_up"    # Icon: Tia sét (⚡)


class PowerUp:
    """Một power-up instance"""

    WIDTH = 45
    HEIGHT = 45
    LIFETIME = 10000  # 10 seconds

    COLORS = {
        PowerUpType.PADDLE_SIZE_UP: (0, 255, 0),      # Xanh lá
        PowerUpType.PADDLE_SIZE_DOWN: (255, 0, 0),    # Đỏ
        PowerUpType.BALL_SPEED_UP: (255, 255, 0),     # Vàng
        PowerUpType.BALL_SPEED_DOWN: (0, 255, 255),   # Cyan
        PowerUpType.PADDLE_SPEED_UP: (255, 165, 0),   # Cam
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
        """Vẽ power-up với icon đặc trưng"""
        if not self.active:
            return

        bg_color = self.COLORS.get(self.type, (255, 255, 255))

        # 1. Vẽ nền (Outer rectangle)
        pygame.draw.rect(win, bg_color, (self.x, self.y, self.WIDTH, self.HEIGHT))

        # 2. Vẽ viền đen (Inner border effect)
        pygame.draw.rect(win, (0, 0, 0),
                        (self.x + 3, self.y + 3, self.WIDTH - 6, self.HEIGHT - 6), 2)

        # 3. Vẽ ICON ở giữa
        center_x = self.x + self.WIDTH // 2
        center_y = self.y + self.HEIGHT // 2

        # Chọn màu icon tương phản với màu nền
        # Nền sáng (Vàng, Cyan, Cam, Xanh) -> Icon Đen
        # Nền tối/đậm (Đỏ) -> Icon Trắng
        icon_color = (0, 0, 0)
        if self.type == PowerUpType.PADDLE_SIZE_DOWN: # Nền đỏ
            icon_color = (255, 255, 255)

        self._draw_icon(win, center_x, center_y, icon_color)

    def _draw_icon(self, win, cx, cy, color):
        """Hàm helper để vẽ các ký hiệu hình học (được vẽ bằng Polygon/Rect đặc)"""

        if self.type == PowerUpType.PADDLE_SIZE_UP:
            # Vẽ dấu CỘNG (+) đậm
            rect_w, rect_h = 14, 36  # Dày hơn để rõ nét
            pygame.draw.rect(win, color, (cx - rect_w//2, cy - rect_h//2, rect_w, rect_h)) # Dọc
            pygame.draw.rect(win, color, (cx - rect_h//2, cy - rect_w//2, rect_h, rect_w)) # Ngang

        elif self.type == PowerUpType.PADDLE_SIZE_DOWN:
            # Vẽ dấu TRỪ (-) đậm
            rect_w, rect_h = 36, 14
            pygame.draw.rect(win, color, (cx - rect_w//2, cy - rect_h//2, rect_w, rect_h))

        elif self.type == PowerUpType.BALL_SPEED_UP:
            # Vẽ 2 hình tam giác đặc hướng phải (Fast Forward icon)
            # Tam giác 1
            t1_p1 = (cx - 15, cy - 12)
            t1_p2 = (cx - 15, cy + 12)
            t1_p3 = (cx - 2, cy)
            pygame.draw.polygon(win, color, [t1_p1, t1_p2, t1_p3])

            # Tam giác 2
            t2_p1 = (cx - 2, cy - 12)
            t2_p2 = (cx - 2, cy + 12)
            t2_p3 = (cx + 11, cy)
            pygame.draw.polygon(win, color, [t2_p1, t2_p2, t2_p3])

        elif self.type == PowerUpType.BALL_SPEED_DOWN:
            # Vẽ 2 hình tam giác đặc hướng trái (Rewind icon)
            # Tam giác 1
            t1_p1 = (cx + 15, cy - 12)
            t1_p2 = (cx + 15, cy + 12)
            t1_p3 = (cx + 2, cy)
            pygame.draw.polygon(win, color, [t1_p1, t1_p2, t1_p3])

            # Tam giác 2
            t2_p1 = (cx + 2, cy - 12)
            t2_p2 = (cx + 2, cy + 12)
            t2_p3 = (cx - 11, cy)
            pygame.draw.polygon(win, color, [t2_p1, t2_p2, t2_p3])

        elif self.type == PowerUpType.PADDLE_SPEED_UP:
            # Vẽ tia sét (⚡) sắc nét hơn
            points = [
                (cx + 8, cy - 18),  # Đỉnh trên phải
                (cx - 2, cy - 2),   # Eo giữa
                (cx + 6, cy - 2),   # Ngạnh phải
                (cx - 8, cy + 18),  # Đáy dưới trái
                (cx + 2, cy + 2),   # Eo giữa dưới
                (cx - 6, cy + 2)    # Ngạnh trái
            ]
            pygame.draw.polygon(win, color, points)


    def check_collision(self, ball_x, ball_y, ball_radius):
        """
        [CẢI TIẾN] Kiểm tra va chạm giữa Hình Tròn (Bóng) và Hình Chữ Nhật (PowerUp).
        Chính xác hơn cách check Box-Box cũ của code gốc.
        """
        if not self.active:
            return False

        # Tìm điểm gần nhất trên hình chữ nhật (PowerUp) so với tâm bóng
        closest_x = max(self.x, min(ball_x, self.x + self.WIDTH))
        closest_y = max(self.y, min(ball_y, self.y + self.HEIGHT))

        # Tính khoảng cách từ tâm bóng đến điểm gần nhất đó
        distance_x = ball_x - closest_x
        distance_y = ball_y - closest_y

        # Dùng bình phương khoảng cách để tối ưu hiệu năng (tránh căn bậc 2)
        distance_squared = (distance_x ** 2) + (distance_y ** 2)

        return distance_squared < (ball_radius ** 2)


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
        self.spawn_threshold = 5  # Giữ nguyên thông số gốc của bạn
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

        # [CẢI TIẾN] Clamp values: Giới hạn chỉ số để tránh lỗi game khi AI train (quá nhanh/quá nhỏ)
        modifiers['paddle_height'] = max(0.5, min(modifiers['paddle_height'], 3.0))
        modifiers['ball_speed'] = max(0.5, min(modifiers['ball_speed'], 2.5))

        return modifiers

    def get_ai_vision_data(self):
        """
        [MỚI] Hàm hỗ trợ NEAT AI:
        Trả về tọa độ powerup để làm input cho Neural Network.
        Returns: [x, y, type_index]
        Nếu không có powerup, trả về [-1, -1, -1]
        """
        if not self.active_powerups:
            return [-1, -1, -1]

        # Lấy powerup đầu tiên
        target = self.active_powerups[0]

        # Map type string sang số để AI hiểu
        type_mapping = {
            PowerUpType.PADDLE_SIZE_UP: 0,
            PowerUpType.PADDLE_SIZE_DOWN: 1,
            PowerUpType.BALL_SPEED_UP: 2,
            PowerUpType.BALL_SPEED_DOWN: 3,
            PowerUpType.PADDLE_SPEED_UP: 4
        }

        type_val = type_mapping.get(target.type, 0)

        return [target.x, target.y, type_val]

    def draw(self, win):
        """Vẽ tất cả power-ups"""
        for powerup in self.active_powerups:
            powerup.draw(win)

    def reset(self):
        """Reset hệ thống"""
        self.active_powerups.clear()
        self.active_effects.clear()
        self.hit_count = 0