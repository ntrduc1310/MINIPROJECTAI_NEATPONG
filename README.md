# 🎮 NEAT PONG AI - Neural Evolution Gaming

**Trí Tuệ Nhân Tạo chơi Pong sử dụng thuật toán NEAT (NeuroEvolution of Augmenting Topologies)**

---

##  Giới Thiệu

Dự án sử dụng thuật toán **NEAT** (NeuroEvolution of Augmenting Topologies) để huấn luyện AI chơi game Pong. NEAT là một phương pháp tiến hóa mạng neural, tự động tối ưu hóa cả cấu trúc mạng lẫn trọng số kết nối.

### ✨ Tính Năng Chính

-  **AI Training**: Huấn luyện AI với thuật toán NEAT evolution
-  **Modern UI**: Giao diện đồ họa hiện đại với gradient, particles, animations
-  **Optimized Performance**: Training siêu nhanh (0.05s/generation, 3800x faster)
-  **Analytics Dashboard**: Theo dõi quá trình huấn luyện real-time
-  **3 Difficulty Levels**: Easy, Medium, Hard AI opponents
-  **Model Management**: Lưu và load trained models
-  **Smooth Gameplay**: 60 FPS với physics chính xác

---



## 🛠️ Cài Đặt & Chạy Project

### 1️ Clone Repository

```bash
git clone https://github.com/ntrduc1310/-NEAT-PONG-AI.git
cd -NEAT-PONG-AI
```

### 2️ Cài Đặt Dependencies

**Yêu cầu**: Python 3.8+

```bash
pip install -r requirements.txt
```

**Dependencies cần thiết**:
- `pygame==2.6.1` - Game engine
- `neat-python==0.92` - NEAT algorithm
- `matplotlib==3.9.3` - Data visualization
- `numpy==2.2.1` - Numerical computing

### 3️ Chạy Game

**Cách 1: Từ thư mục gốc**
```bash
cd src
python main.py
```

**Cách 2: Chạy trực tiếp**
```bash
python src/main.py
```

---

##  Hướng Dẫn Sử Dụng

### Menu Chính

Khi khởi động, bạn sẽ thấy menu với các options:

1. **>> Train AI Network** - Huấn luyện AI mới
2. **[1] Easy AI** - Chơi với AI level dễ
3. **[2] Medium AI** - Chơi với AI level trung bình  
4. **[3] Hard AI** - Chơi với AI level khó
5. **< Quit >** - Thoát game

###  Huấn Luyện AI

1. Chọn option **">> Train AI Network"**
2. Chọn difficulty level (easy/medium/hard)
3. Chờ training hoàn thành (~4 seconds cho 50 generations)
4. Model được lưu tự động vào thư mục `models/`

**Training Features**:
- Real-time dashboard hiển thị fitness score
- Logs được lưu vào `logs/` folder
- Model tốt nhất được lưu với config

###  Chơi Game

**Controls**:
- `W` - Di chuyển lên
- `S` - Di chuyển xuống
- `P` - Pause game
- `ESC` - Quit về menu

**Luật chơi**:
- Người chơi (bên trái) vs AI (bên phải)
- Điểm tăng khi đối thủ miss ball
- First to 10 points wins

---

##  Cấu Trúc Project

```
NEAT-Pong-Python/
├── config/
│   └── config-feedforward.txt      # NEAT algorithm configuration
├── src/
│   ├── ai_engine/                  # AI & NEAT engine
│   │   ├── trainer.py              # Training orchestration
│   │   ├── predictor.py            # AI prediction logic
│   │   └── model_manager.py        # Model save/load
│   ├── game_engine/                # Game mechanics
│   │   ├── game_manager.py         # Core game loop
│   │   ├── ball.py                 # Ball physics
│   │   └── paddle.py               # Paddle mechanics
│   ├── ui/                         # User interface
│   │   ├── menu.py                 # Main menu system
│   │   └── visuals.py              # Visual effects
│   ├── features/                   # Additional features
│   │   ├── analytics.py            # Training analytics
│   │   └── powerups.py             # Power-up system
│   ├── models/                     # Saved AI models
│   ├── logs/                       # Training logs
│   └── main.py                     # Entry point
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

##  NEAT Configuration

File config tại `config/config-feedforward.txt`:

**Key Parameters**:
- `pop_size = 30` - Population size (số lượng genomes mỗi generation)
- `fitness_threshold = 400` - Target fitness để dừng training
- `num_inputs = 3` - Ball position (y), ball velocity (y), paddle position (y)
- `num_outputs = 1` - Paddle movement (-1 to 1)
- `activation_default = tanh` - Activation function

**Network Evolution**:
- Tự động thêm/xóa nodes và connections
- Mutation rates được tối ưu cho game Pong
- Compatibility threshold để maintain diversity

---

##  Performance Optimization

Dự án đã được optimize để training **cực nhanh**:

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Time/Generation | ~190s | ~0.05s | **3800x faster** |
| Population Size | 50 | 30 | Reduced 40% |
| Max Hits/Game | unlimited | 15 | Faster convergence |
| Game Timeout | unlimited | 5s | Prevent infinite loops |
| FPS Cap | 60 | None | Maximum speed |

**Training Speed**: 50 generations trong ~4 giây!

---

##  Training Analytics

Mỗi lần training sẽ tạo 2 files trong `logs/`:

1. **generation_[timestamp].csv** - Generation-level stats
   - Generation number
   - Best fitness
   - Average fitness
   - Species count
   - Time elapsed

2. **genome_[timestamp].csv** - Genome-level details
   - Individual genome IDs
   - Fitness scores
   - Species assignment

**Sử dụng data**:
```python
import pandas as pd
df = pd.read_csv('logs/generation_20251219_143521.csv')
print(df['best_fitness'].max())
```

---

##  UI Features

### Visual Effects
- **Gradient Backgrounds** - Modern color schemes
- **Particle Systems** - 50+ animated particles
- **Smooth Animations** - Title floating, button scaling
- **Glow Effects** - Score highlights, button hovers
- **Professional Typography** - Clean, readable fonts

### Color Scheme
- Player (You): Blue (#4A90E2)
- AI Opponent: Red (#E74C3C)
- Background: Dark gradient (#1A1A2E → #16213E)
- Accents: White/Green/Gold

---

## Troubleshooting

### Lỗi: "No module named 'neat'"
```bash
pip install neat-python
```

### Lỗi: "pygame not found"
```bash
pip install pygame
```

### Lỗi: "Model not found"
- Cần train AI trước khi chơi
- Chọn option ">> Train AI Network" trong menu

### Training quá chậm
- Đảm bảo đang dùng code mới nhất
- Check file config có `pop_size = 30`

### Game bị lag
- Close các ứng dụng khác
- Giảm population size trong config

---

##  Tài Liệu Tham Khảo

- [NEAT Algorithm Paper](http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf)
- [NEAT-Python Documentation](https://neat-python.readthedocs.io/)
- [Pygame Documentation](https://www.pygame.org/docs/)

---

##  License

MIT License - Free to use for educational purposes

---

##  Credits

- **NEAT Algorithm**: Kenneth O. Stanley
- **Original Tutorial**: Tech With Tim
- **Team Project**: TV1, TV2, TV3, TV4
- **University**: [Your University Name]

---


