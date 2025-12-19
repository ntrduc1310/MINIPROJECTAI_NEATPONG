"""
Ball Predictor - TV1 (Trí Hoằng)
Dự đoán quỹ đạo bóng với physics đầy đủ
"""
import math


class BallPredictor:
    """
    Predictor nâng cao cho AI
    Dự đoán vị trí bóng trong tương lai
    """
    
    def __init__(self, window_width, window_height, paddle_width, paddle_height):
        """
        Khởi tạo predictor
        
        Args:
            window_width: Chiều rộng window
            window_height: Chiều cao window
            paddle_width: Chiều rộng vợt
            paddle_height: Chiều cao vợt
        """
        self.window_width = window_width
        self.window_height = window_height
        self.paddle_width = paddle_width
        self.paddle_height = paddle_height
    
    def predict_ball_position(self, ball_x, ball_y, ball_vx, ball_vy, 
                             ball_radius, time_steps=10, paddle_x=None, paddle_y=None):
        """
        Dự đoán vị trí bóng sau N time steps với đầy đủ collision physics
        
        Args:
            ball_x, ball_y: Vị trí hiện tại
            ball_vx, ball_vy: Vận tốc hiện tại
            ball_radius: Bán kính bóng
            time_steps: Số bước mô phỏng
            paddle_x, paddle_y: Vị trí vợt (optional)
        
        Returns:
            tuple: (pred_x, pred_y, pred_vx, pred_vy)
        """
        # Copy để không thay đổi giá trị gốc
        pred_x = ball_x
        pred_y = ball_y
        pred_vx = ball_vx
        pred_vy = ball_vy
        
        for _ in range(time_steps):
            # Di chuyển
            pred_x += pred_vx
            pred_y += pred_vy
            
            # Va chạm tường trên/dưới
            if pred_y + ball_radius >= self.window_height:
                pred_y = self.window_height - ball_radius
                pred_vy *= -1
            elif pred_y - ball_radius <= 0:
                pred_y = ball_radius
                pred_vy *= -1
            
            # Va chạm vợt (nếu có thông tin)
            if paddle_x is not None and paddle_y is not None:
                if pred_vx < 0:  # Bóng đi về bên trái
                    if (pred_y >= paddle_y and 
                        pred_y <= paddle_y + self.paddle_height):
                        if pred_x - ball_radius <= paddle_x + self.paddle_width:
                            # Va chạm vợt
                            pred_x = paddle_x + self.paddle_width + ball_radius
                            pred_vx *= -1
                            
                            # Tính góc bounce
                            middle_y = paddle_y + self.paddle_height / 2
                            difference_in_y = middle_y - pred_y
                            reduction_factor = (self.paddle_height / 2) / abs(ball_vx)
                            pred_vy = -1 * (difference_in_y / reduction_factor)
        
        return (pred_x, pred_y, pred_vx, pred_vy)
    
    def predict_y_at_x(self, ball_x, ball_y, ball_vx, ball_vy, 
                       ball_radius, target_x, max_bounces=3):
        """
        Dự đoán vị trí Y khi bóng đến vị trí X
        Quan trọng cho AI positioning
        
        Args:
            ball_x, ball_y: Vị trí hiện tại
            ball_vx, ball_vy: Vận tốc hiện tại
            ball_radius: Bán kính
            target_x: Vị trí X cần predict
            max_bounces: Số lần bounce tối đa
        
        Returns:
            float: Vị trí Y dự đoán hoặc None
        """
        if ball_vx == 0:
            return None
        
        pred_x = ball_x
        pred_y = ball_y
        pred_vx = ball_vx
        pred_vy = ball_vy
        bounces = 0
        
        max_iterations = 1000
        iterations = 0
        
        while iterations < max_iterations and bounces <= max_bounces:
            iterations += 1
            
            # Tính thời gian đến target_x
            if pred_vx == 0:
                return None
            
            time_to_target = (target_x - pred_x) / pred_vx
            
            # Nếu target nằm trước mặt
            if time_to_target > 0:
                # Tính Y tương lai
                future_y = pred_y + pred_vy * time_to_target
                
                # Check bounce với tường
                if future_y - ball_radius < 0:
                    # Bounce tường trên
                    time_to_wall = (ball_radius - pred_y) / pred_vy
                    pred_x += pred_vx * time_to_wall
                    pred_y = ball_radius
                    pred_vy *= -1
                    bounces += 1
                elif future_y + ball_radius > self.window_height:
                    # Bounce tường dưới
                    time_to_wall = (self.window_height - ball_radius - pred_y) / pred_vy
                    pred_x += pred_vx * time_to_wall
                    pred_y = self.window_height - ball_radius
                    pred_vy *= -1
                    bounces += 1
                else:
                    # Không có bounce, return kết quả
                    return future_y
            else:
                # Bóng đang đi xa target
                return None
        
        # Timeout hoặc quá nhiều bounces
        return pred_y
    
    def get_intercept_point(self, ball_x, ball_y, ball_vx, ball_vy, 
                           ball_radius, paddle_x, is_left_paddle=True):
        """
        Tính vị trí tối ưu của vợt để đón bóng
        
        Args:
            ball_x, ball_y: Vị trí bóng
            ball_vx, ball_vy: Vận tốc bóng
            ball_radius: Bán kính
            paddle_x: Vị trí X của vợt
            is_left_paddle: True nếu là vợt trái
        
        Returns:
            float: Vị trí Y tối ưu cho center của vợt
        """
        # Xác định target X dựa trên vợt nào
        if is_left_paddle:
            target_x = paddle_x + self.paddle_width
        else:
            target_x = paddle_x
        
        # Dự đoán Y tại vị trí vợt
        predicted_y = self.predict_y_at_x(
            ball_x, ball_y, ball_vx, ball_vy, 
            ball_radius, target_x
        )
        
        if predicted_y is None:
            # Fallback: follow ball Y
            return ball_y
        
        # Clamp trong giới hạn hợp lệ
        min_y = self.paddle_height / 2
        max_y = self.window_height - self.paddle_height / 2
        
        return max(min_y, min(max_y, predicted_y))
    
    def get_optimal_action(self, paddle_y, ball_x, ball_y, ball_vx, ball_vy, 
                          ball_radius, paddle_x, is_left_paddle=True):
        """
        Trả về action tối ưu cho AI (0=stay, 1=up, 2=down)
        
        Args:
            paddle_y: Vị trí Y hiện tại của vợt
            ball_x, ball_y: Vị trí bóng
            ball_vx, ball_vy: Vận tốc bóng
            ball_radius: Bán kính
            paddle_x: Vị trí X vợt
            is_left_paddle: True nếu vợt trái
        
        Returns:
            int: 0 (stay), 1 (up), 2 (down)
        """
        target_y = self.get_intercept_point(
            ball_x, ball_y, ball_vx, ball_vy,
            ball_radius, paddle_x, is_left_paddle
        )
        
        # Threshold để tránh rung
        threshold = 10
        
        paddle_center = paddle_y + self.paddle_height / 2
        
        if abs(target_y - paddle_center) < threshold:
            return 0  # Stay
        elif target_y < paddle_center:
            return 1  # Move up
        else:
            return 2  # Move down
