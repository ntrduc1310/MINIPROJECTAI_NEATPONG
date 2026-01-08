# NEAT Pong - AI Training System

Dự án huấn luyện AI chơi game Pong sử dụng thuật toán NEAT (NeuroEvolution of Augmenting Topologies).

## Giới thiệu

Đây là project môn học về AI, ứng dụng thuật toán NEAT để train một AI agent có khả năng chơi game Pong. NEAT là một dạng genetic algorithm có thể tiến hóa cả cấu trúc (topology) và trọng số (weights) của neural network, khác với các phương pháp thông thường chỉ train weights.

**Điểm đặc biệt:**
- AI tự học cách chơi từ đầu, không cần dữ liệu training sẵn
- Network structure tự động phát triển từ đơn giản đến phức tạp
- Có 3 mức độ khó: Easy, Medium, Hard

## Yêu cầu

**Phần mềm:**
- Python 3.8+
- pip

**Thư viện:**
- pygame
- neat-python
- numpy, pandas, matplotlib (cho analytics)

## Cài đặt

1. Clone project:
```bash
git clone https://github.com/your-username/NEAT-Pong-Python.git
cd NEAT-Pong-Python
```

2. Cài đặt thư viện:
```bash
pip install -r requirements.txt
```

3. Chạy game:
```bash
cd src
python main.py
```

## Cách sử dụng

### Train AI mới

Chọn menu "Train AI" và chọn độ khó:
- **Easy**: 10 generations (~5 phút)
- **Medium**: 25 generations (~15 phút)  
- **Hard**: 50 generations (~30 phút)

Model được lưu tự động trong folder `models/`.

### Chơi với AI

Chọn "Play vs [Difficulty]" để chơi với AI đã train.

**Controls:**
- W/S: Di chuyển paddle
- P: Pause
- ESC: Thoát về menu

### Xem logs training

Dữ liệu training được lưu trong `logs/` dưới dạng CSV. Có thể dùng `visualize_full_report.py` để tạo biểu đồ.

## Cấu trúc project

```
NEAT-Pong-Python/
├── config/
│   └── config-feedforward.txt    # Cấu hình NEAT
├── src/
│   ├── main.py                   # File chính
│   ├── ai_engine/                # AI logic
│   │   ├── trainer.py           # Training system
│   │   ├── ai_controller.py     # AI decision making
│   │   └── model_manager.py     # Load/save models
│   ├── game_engine/              # Game mechanics
│   │   ├── game_manager.py      # Game loop
│   │   ├── paddle.py            
│   │   └── ball.py              
│   ├── features/                 # Features bổ sung
│   │   ├── analytics.py         # Training logs
│   │   └── powerups.py          # Power-ups
│   └── ui/                       # Giao diện
│       ├── menu.py
│       └── visuals.py
└── requirements.txt
```

## Cách hoạt động của NEAT

### Input (3 neurons)
- Vị trí X của bóng
- Vị trí Y của bóng  
- Vị trí Y của paddle AI

### Output (3 neurons)
- Đứng yên
- Di chuyển lên
- Di chuyển xuống

### Fitness function
```python
fitness = số_lần_đập_bóng * 10 + thời_gian_sống - penalty
```

### Quá trình evolution
1. Bắt đầu với network đơn giản (3 input -> 3 output, không có hidden layer)
2. Mỗi generation, các genomes được đánh giá qua fitness
3. Các genome tốt nhất được chọn để lai ghép (crossover)
4. Random mutation: thêm/bớt nodes và connections
5. Lặp lại cho N generations

## Team phát triển

| Thành viên | Vai trò | Module phụ trách |
|------------|---------|------------------|
| TV1 - Trí Hoằng | AI/ML | `ai_engine/*` |
| TV2 - Dũng | Game Physics | `game_engine/paddle.py`, `game_engine/ball.py` |
| TV3 - Trọng Đức | Game Engine & Analytics | `game_engine/game_manager.py`, `features/analytics.py` |
| TV4 - Bảo | UI/UX | `ui/*` |

## Performance

Kết quả test trên máy i5-8250U, 8GB RAM:

| Độ khó | Generations | Thời gian | Win rate vs người |
|--------|-------------|-----------|-------------------|
| Easy | 10 | ~5 phút | 40-50% |
| Medium | 25 | ~15 phút | 60-70% |
| Hard | 50 | ~30 phút | 80-90% |

## Troubleshooting

**Lỗi "ModuleNotFoundError":**
```bash
pip install neat-python pygame
```

**Training quá chậm:**
- Giảm population size trong `config/config-feedforward.txt`
- Giảm số generations

**AI không load:**
- Kiểm tra folder `models/` có file `.pkl` không
- Chạy lại training nếu cần

## Tài liệu tham khảo

- Paper NEAT gốc: [Stanley & Miikkulainen, 2002](http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf)
- NEAT-Python docs: https://neat-python.readthedocs.io/
- Pygame docs: https://www.pygame.org/docs/

## License

MIT License - xem file [LICENSE](LICENSE) để biết thêm chi tiết.
