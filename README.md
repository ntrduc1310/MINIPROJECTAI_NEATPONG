# NEAT Pong AI

Ứng dụng game Pong với AI được huấn luyện bằng thuật toán NEAT (NeuroEvolution of Augmenting Topologies).

## Giới thiệu

NEAT là thuật toán tiến hóa mạng neural cho phép AI tự động học cách chơi Pong thông qua quá trình tiến hóa. Thuật toán không chỉ tối ưu trọng số mà còn tự động xây dựng cấu trúc mạng neural phù hợp.

### Tính năng

- Huấn luyện AI với thuật toán NEAT evolution
- Giao diện đồ họa với hiệu ứng gradient và particles
- Tốc độ training tối ưu (0.05s/generation)
- Dashboard theo dõi quá trình training
- 3 mức độ khó: Easy, Medium, Hard
- Lưu và load trained models
- Gameplay mượt mà 60 FPS
- Hỗ trợ fullscreen với auto-scaling


## Cài đặt

### Yêu cầu hệ thống

- Python 3.8 trở lên
- Pygame 2.6.1
- neat-python 0.92
- matplotlib 3.9.3
- numpy 2.2.1

### Hướng dẫn cài đặt

1. Clone repository:
```bash
git clone https://github.com/ntrduc1310/MINIPROJECTAI_NEATPONG.git
cd MINIPROJECTAI_NEATPONG
```

2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

3. Chạy chương trình:
```bash
cd src
python main.py
```


## Hướng dẫn sử dụng

### Menu chính

Chương trình cung cấp các tùy chọn sau:

- [T] Train AI Network - Huấn luyện AI mới
- [E] Easy AI - Chơi với AI mức độ dễ
- [M] Medium AI - Chơi với AI mức độ trung bình
- [H] Hard AI - Chơi với AI mức độ khó
- [Q] Quit - Thoát chương trình

Phím tắt:
- F11: Bật/tắt fullscreen
- ESC: Thoát fullscreen
- Theme toggle: Chuyển đổi giao diện sáng/tối

### Huấn luyện AI

1. Chọn "Train AI Network" từ menu
2. Chọn mức độ khó (easy/medium/hard)
3. Quá trình training sẽ tự động chạy (khoảng 4 giây cho 50 generations)
4. Model được lưu tự động vào thư mục models/

Trong quá trình training:
- Dashboard hiển thị fitness score theo thời gian thực
- Logs được lưu vào thư mục logs/ với timestamp
- Model tốt nhất tự động được lưu

### Chơi game

Phím điều khiển:
- W: Di chuyển lên
- S: Di chuyển xuống
- P: Pause/Resume
- ESC: Quay về menu

Luật chơi:
- Người chơi (paddle trái) đối đầu AI (paddle phải)
- Mỗi lần đối thủ miss ball được 1 điểm
- Người chơi đạt 10 điểm trước sẽ thắng


## Cấu trúc project

```
NEAT-Pong-Python/
├── config/
│   └── config-feedforward.txt      # Cấu hình NEAT algorithm
├── src/
│   ├── ai_engine/                  # Module AI và NEAT
│   │   ├── trainer.py              # Quản lý training
│   │   ├── predictor.py            # Logic prediction
│   │   └── model_manager.py        # Lưu/load model
│   ├── game_engine/                # Game mechanics
│   │   ├── game_manager.py         # Game loop chính
│   │   ├── ball.py                 # Vật lý bóng
│   │   └── paddle.py               # Cơ chế paddle
│   ├── ui/                         # Giao diện người dùng
│   │   ├── menu.py                 # Menu system
│   │   └── visuals.py              # Hiệu ứng visual
│   ├── features/                   # Tính năng bổ sung
│   │   ├── analytics.py            # Phân tích training
│   │   └── powerups.py             # Power-up system
│   ├── models/                     # AI models đã lưu
│   ├── logs/                       # Training logs
│   └── main.py                     # Entry point
├── requirements.txt
└── README.md
```


## Cấu hình NEAT

File config tại config/config-feedforward.txt chứa các tham số chính:

### Tham số quan trọng

- pop_size = 30: Kích thước population mỗi generation
- fitness_threshold = 400: Ngưỡng fitness để dừng training
- num_inputs = 3: Vị trí bóng (y), vận tốc bóng (y), vị trí paddle (y)
- num_outputs = 1: Hướng di chuyển paddle (-1 đến 1)
- activation_default = tanh: Hàm activation

### Cơ chế evolution

NEAT tự động điều chỉnh cấu trúc mạng trong quá trình training:
- Thêm/xóa nodes và connections
- Mutation rates được tối ưu cho game Pong
- Compatibility threshold duy trì diversity trong population


## Tối ưu hóa performance

Project đã được tối ưu để đạt tốc độ training cao:

| Metric | Trước | Sau | Cải thiện |
|--------|-------|-----|-----------|
| Thời gian/Generation | ~190s | ~0.05s | 3800x |
| Population Size | 50 | 30 | Giảm 40% |
| Max Hits/Game | unlimited | 15 | Hội tụ nhanh hơn |
| Game Timeout | unlimited | 5s | Tránh vòng lặp vô hạn |
| FPS Cap | 60 | None | Tốc độ tối đa |

Kết quả: Training 50 generations trong khoảng 4 giây.


## Training analytics

Mỗi lần training tạo 2 file CSV trong thư mục logs/:

### generation_[timestamp].csv
Thống kê theo generation:
- Generation number
- Best fitness
- Average fitness
- Species count
- Time elapsed

### genome_[timestamp].csv
Chi tiết từng genome:
- Genome ID
- Fitness score
- Species assignment

Ví dụ phân tích data:
```python
import pandas as pd
df = pd.read_csv('logs/generation_20251219_143521.csv')
print(df['best_fitness'].max())
```


## Giao diện

### Hiệu ứng visual
- Gradient backgrounds
- Particle system (50+ particles)
- Smooth animations
- Glow effects cho score và buttons
- Typography rõ ràng dễ đọc

### Bảng màu
- Player: Blue (#4A90E2)
- AI: Red (#E74C3C)
- Background: Dark gradient (#1A1A2E → #16213E)
- Accents: White/Green/Gold


## Xử lý lỗi thường gặp

### Lỗi thiếu module
```bash
# No module named 'neat'
pip install neat-python

# pygame not found
pip install pygame
```

### Lỗi không tìm thấy model
Cần train AI trước khi chơi. Chọn "Train AI Network" từ menu để tạo model mới.

### Training chậm
Kiểm tra:
- Đang sử dụng code mới nhất
- File config có pop_size = 30
- Không chạy nhiều ứng dụng nặng khác

### Game bị lag
- Đóng các ứng dụng không cần thiết
- Giảm population size trong file config nếu cần


## Tài liệu tham khảo

- NEAT Algorithm Paper: http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf
- NEAT-Python Documentation: https://neat-python.readthedocs.io/
- Pygame Documentation: https://www.pygame.org/docs/

## License

MIT License

## Nhóm phát triển

Project: NEAT Pong AI Training System
Team: TV1 (AI/ML), TV2 (Physics), TV3 (Engine & Analytics), TV4 (UI/Graphics)
Powered by NEAT-Python & Pygame
