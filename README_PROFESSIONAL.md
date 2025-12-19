# 🎮 NEAT Pong - Professional Edition

**Neural Evolution of Augmenting Topologies applied to Pong Game**

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![NEAT-Python](https://img.shields.io/badge/NEAT--Python-0.92+-green.svg)](https://neat-python.readthedocs.io/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-red.svg)](https://www.pygame.org/)

---

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Team Responsibilities](#team-responsibilities)
- [Documentation](#documentation)
- [License](#license)

---

## 🌟 Overview

NEAT Pong is a professional-grade implementation of the classic Pong game enhanced with AI trained using **NEAT (NeuroEvolution of Augmenting Topologies)**. This project demonstrates advanced machine learning techniques, game development best practices, and modular software architecture.

### Key Highlights
- ✨ **AI Training**: Train neural networks through evolution without backpropagation
- 🎯 **3 Difficulty Levels**: Easy, Medium, Hard AI opponents
- ⚡ **Power-ups System**: Dynamic gameplay with 5 different power-ups
- 📊 **Real-time Analytics**: Live training visualization and comprehensive logging
- 🎨 **Modern UI**: Professional menu system and visual effects

---

## 🚀 Features

### AI Engine (TV1 - Trí Hoằng)
- **Ball Trajectory Prediction**: Advanced physics simulation for AI decision-making
- **Model Management**: Save/load AI models with different difficulty levels
- **NEAT Training**: Evolutionary algorithm for network topology optimization

### Game Engine (TV2 - Dũng)
- **Core Game Logic**: Physics, collision detection, scoring
- **Power-ups System**: 
  - 🟢 Paddle Size Up
  - 🔴 Paddle Size Down
  - 🟡 Ball Speed Up
  - 🔵 Ball Speed Down
  - 🟠 Paddle Speed Up

### Analytics (TV3 - Trọng Đức)
- **Training Logger**: CSV-based logging for generations and genomes
- **Dashboard**: Real-time visualization of training progress
- **Statistics**: Fitness tracking, generation times, species evolution

### UI & Integration (TV4 - Bảo)
- **Main Menu**: Clean, intuitive navigation
- **Visual Effects**: Particles, screen shake, score animations
- **Asset Management**: Font loading and resource management

---

## 📁 Project Structure

```
NEAT-Pong-Python/
├── src/                          # Source code
│   ├── game_engine/             # Game logic (TV2)
│   │   ├── __init__.py
│   │   ├── ball.py              # Ball physics
│   │   ├── paddle.py            # Paddle control
│   │   └── game_manager.py      # Game loop & collisions
│   │
│   ├── ai_engine/               # AI components (TV1)
│   │   ├── __init__.py
│   │   ├── predictor.py         # Ball trajectory prediction
│   │   ├── model_manager.py     # Save/load models
│   │   └── trainer.py           # NEAT training logic
│   │
│   ├── features/                # Extended features
│   │   ├── __init__.py
│   │   ├── powerups.py          # Power-up system (TV2)
│   │   └── analytics.py         # Training analytics (TV3)
│   │
│   ├── ui/                      # User interface (TV4)
│   │   ├── __init__.py
│   │   ├── menu.py              # Main menu
│   │   └── visuals.py           # Effects & asset manager
│   │
│   ├── __init__.py
│   └── main.py                  # Main entry point
│
├── config/                      # Configuration files
│   └── config-feedforward.txt   # NEAT config
│
├── models/                      # Saved AI models
│   ├── easy_model.pkl
│   ├── medium_model.pkl
│   └── hard_model.pkl
│
├── logs/                        # Training logs
│   ├── generation_*.csv
│   └── genome_*.csv
│
├── assets/                      # Game assets
│   └── fonts/
│
├── docs/                        # Documentation
│   ├── DOCUMENTATION.md
│   ├── QUICKSTART.md
│   └── TEAM_RESPONSIBILITIES.md
│
├── requirements.txt
└── README.md
```

---

## 💻 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup

1. **Clone repository** (or download source code)
```bash
cd NEAT-Pong-Python
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Verify installation**
```bash
python -c "import pygame, neat; print('✅ All dependencies installed')"
```

---

## 🎮 Quick Start

### Run the Game

```bash
cd src
python main.py
```

### Menu Options

1. **Train AI** - Train a new AI model using NEAT algorithm
2. **Play vs Easy AI** - Play against easy difficulty AI
3. **Play vs Medium AI** - Play against medium difficulty AI
4. **Play vs Hard AI** - Play against hard difficulty AI
5. **Quit** - Exit the application

### Controls

**In-Game:**
- `W` - Move left paddle up
- `S` - Move left paddle down
- `P` - Pause game
- `ESC` - Quit to menu

**Training:**
- `ESC` - Stop training early (saves current best)

---

## 👥 Team Responsibilities

### TV1: Trí Hoằng - AI Engine
**Modules**: `ai_engine/`
- Ball trajectory prediction algorithm
- AI model management (save/load)
- NEAT training orchestration
- Neural network integration

### TV2: Dũng - Game Engine & Power-ups
**Modules**: `game_engine/`, `features/powerups.py`
- Core game physics and collision
- Ball and paddle mechanics
- Power-up system implementation
- Game state management

### TV3: Trọng Đức - Analytics & Dashboard
**Modules**: `features/analytics.py`
- Training data logging (CSV)
- Real-time dashboard visualization
- Statistics calculation
- NEAT reporter integration

### TV4: Bảo - UI & Integration
**Modules**: `ui/`, `src/main.py`
- Main menu system
- Visual effects (particles, shake, etc.)
- Asset management
- Module integration in main.py

---

## 📚 Documentation

Comprehensive documentation available in `docs/`:

- **[DOCUMENTATION.md](docs/DOCUMENTATION.md)** - Complete technical documentation
- **[QUICKSTART.md](docs/QUICKSTART.md)** - Quick setup guide
- **[TEAM_RESPONSIBILITIES.md](docs/TEAM_RESPONSIBILITIES.md)** - Detailed team tasks

### Code Documentation

All modules include detailed docstrings:

```python
"""
Module description

Classes:
    ClassName - Purpose
    
Functions:
    function_name() - Purpose
"""
```

---

## 🔧 Configuration

NEAT configuration in `config/config-feedforward.txt`:

```ini
[NEAT]
fitness_criterion     = max      # Maximize fitness
fitness_threshold     = 400      # Target fitness
pop_size              = 50       # Population size

[DefaultGenome]
num_inputs            = 5        # Ball x, y, vx, vy, paddle y
num_outputs           = 1        # Paddle movement
num_hidden            = 2        # Hidden nodes
activation_default    = relu     # Activation function
```

Adjust these values to experiment with different training behaviors.

---

## 📊 Training Output

Training generates logs in `logs/`:

**generation_TIMESTAMP.csv:**
```csv
Generation,BestFitness,AvgFitness,MinFitness,StdDev,SpeciesCount,Duration(s)
1,45.2,23.1,5.0,12.3,8,2.5
2,52.7,28.4,8.1,13.1,7,2.3
...
```

**genome_TIMESTAMP.csv:**
```csv
Generation,GenomeID,Fitness,Nodes,Connections
1,1,45.2,7,12
1,2,32.1,6,10
...
```

---

## 🎯 Performance Tips

### Training
- Start with 25-50 generations for testing
- Increase `pop_size` for better exploration (slower)
- Adjust `fitness_threshold` based on desired performance

### Gameplay
- Easy AI: Quick reactions, good for beginners
- Medium AI: Balanced difficulty
- Hard AI: Predictive, challenging gameplay

---

## 🐛 Troubleshooting

### Common Issues

**ModuleNotFoundError: No module named 'neat'**
```bash
pip install neat-python
```

**pygame.error: Font not found**
- Fonts are optional, default font will be used
- Add custom fonts to `assets/fonts/`

**No AI model found**
- Train an AI first using "Train AI" option
- Models saved in `models/` directory

---

## 📈 Future Enhancements

- [ ] Multiplayer mode (2 players)
- [ ] Tournament mode (AI vs AI)
- [ ] Custom training parameters UI
- [ ] Sound effects and music
- [ ] Replay system
- [ ] Web deployment (Pygame Web)

---

## 📝 License

This project is created for educational purposes as part of an AI/ML course project.

**Team Members:**
- TV1: Trí Hoằng
- TV2: Dũng  
- TV3: Trọng Đức
- TV4: Bảo

---

## 🙏 Acknowledgments

- **NEAT-Python**: Kenneth O. Stanley's NEAT implementation
- **Pygame**: Cross-platform game development
- **Python Community**: Excellent libraries and documentation

---

## 📞 Support

For questions or issues:
1. Check documentation in `docs/`
2. Review code comments and docstrings
3. Consult team members based on module responsibility

---

**Made with ❤️ by TV1, TV2, TV3, TV4**

*Demonstrating the power of evolutionary algorithms in game AI!*
