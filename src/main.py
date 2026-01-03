"""
NEAT Pong - Main Entry Point
Tích hợp tất cả modules: Game Engine, AI Engine, Features, UI
Team: TV1 (Trí Hoằng), TV2 (Dũng), TV3 (Trọng Đức), TV4 (Bảo)
"""
import pygame
import neat
import os
import sys

# Import game engine (TV2 - Dũng)
from game_engine.game_manager import GameManager
from game_engine.paddle import Paddle
from game_engine.ball import Ball

# Import AI engine (TV1 - Trí Hoằng)
from ai_engine.trainer import NEATTrainer
from ai_engine.model_manager import get_model_manager
from ai_engine.predictor import BallPredictor

# Import features (TV2 & TV3)
from features.powerups import PowerUpManager
from features.analytics import TrainingAnalytics, TrainingDashboard, NEATReporter

# Import UI (TV4 - Bảo)
from ui.menu import show_menu
from ui.visuals import VisualEffects, ScoreDisplay, get_asset_manager


# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
# Get config path (relative to this file's parent directory)
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "config-feedforward.txt")


def train_ai(config_path, target_difficulty="medium"):
    """
    Train AI với NEAT algorithm theo độ khó cụ thể

    Args:
        config_path: Đường dẫn config file
        target_difficulty: 'easy', 'medium', hoặc 'hard'
    """
    print("\n" + "="*50)
    print(f"NEURAL NETWORK TRAINING - TARGET: {target_difficulty.upper()}")
    print("="*50)

    # Kiểm tra config file
    if not os.path.exists(config_path):
        print(f"[ERROR] Config file not found: {config_path}")
        print("Please ensure config file exists in config/ directory")
        return

    # Load NEAT config
    try:
        config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path
        )
        print(f"[OK] Config loaded from: {config_path}")
    except Exception as e:
        print(f"[ERROR] Error loading config: {e}")
        return

    # Initialize analytics (TV3 - Trọng Đức)
    analytics = TrainingAnalytics()

    # Initialize trainer (TV1 - Trí Hoằng)
    # show_dashboard=False for maximum speed on Colab
    trainer = NEATTrainer(
        config,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        show_dashboard=False
    )
    print(f"[OK] Trainer initialized")

    # Lấy số thế hệ cần train từ ModelManager
    model_manager = get_model_manager()
    generations = model_manager.get_training_generations(target_difficulty)

    # Add reporter
    reporter = NEATReporter(analytics)

    # Train
    print(f"\n[INFO] Starting training for {generations} generations...")
    print("Press ESC to stop training early")
    print("-" * 50)

    try:
        # Train với số thế hệ cụ thể cho độ khó đó
        best_genome = trainer.train_ai(reporter=reporter, generations=generations)

        if best_genome:
            print("\n" + "="*50)
            print("[SUCCESS] AI EVOLUTION COMPLETE!")
            print("="*50)
            print(f"Best Neural Network Fitness: {best_genome.fitness:.2f}")

            # LƯU MODEL ĐÚNG VỚI TÊN ĐỘ KHÓ ĐÃ CHỌN
            model_manager.save_model(best_genome, config, target_difficulty)
            print(f"[SAVED] Neural Network saved as: '{target_difficulty.upper()}' AI")

            # Analytics summary
            summary = analytics.get_summary()
            print(f"\nEvolution Statistics:")
            print(f"   Generations Evolved: {summary['total_generations']}")
            print(f"   Peak Performance: {summary['best_fitness']:.2f}")
            print(f"   Training Duration: {summary['total_time']:.2f}s")
            print(f"   Data Logs: logs/")

    except KeyboardInterrupt:
        print("\n[!] Training interrupted by user")
    except Exception as e:
        print(f"\n[ERROR] Training error: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "="*50)
    input("Press Enter to return to menu...")


def play_vs_ai(difficulty="medium"):
    """
    Chơi với AI

    Args:
        difficulty: 'easy', 'medium', 'hard'
    """
    print(f"\n[AI] Loading {difficulty.upper()} Neural Network AI...")

    # Load AI model (TV1 - Trí Hoằng)
    model_manager = get_model_manager()
    result = model_manager.load_ai_network(difficulty)

    if result is None:
        print(f"[ERROR] No {difficulty} AI model found!")
        print(f"Please train the '{difficulty}' AI first from the menu!")
        input("Press Enter to return to menu...")
        return

    ai_net, config = result
    print(f"[READY] Neural Network Active: {difficulty.upper()} AI")

    # Initialize pygame
    pygame.init()
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(f"NEAT Pong - vs {difficulty.upper()} AI")
    clock = pygame.time.Clock()

    # Initialize game (TV2 - Dũng)
    game = GameManager(win, WINDOW_WIDTH, WINDOW_HEIGHT)

    # Initialize features
    powerup_manager = PowerUpManager(WINDOW_WIDTH, WINDOW_HEIGHT)
    predictor = BallPredictor(WINDOW_WIDTH, WINDOW_HEIGHT, Paddle.WIDTH, Paddle.HEIGHT)

    # Initialize UI (TV4 - Bảo)
    effects = VisualEffects()
    score_display = ScoreDisplay(WINDOW_WIDTH, WINDOW_HEIGHT)

    # Game loop
    running = True
    paused = False
    font = pygame.font.Font(None, 40)

    print("\n[GAME] BATTLE VS AI STARTED!")
    print("Controls:")
    print("  W: Move Up")
    print("  S: Move Down")
    print("  P: Pause")
    print("  ESC: Quit\n")

    while running:
        clock.tick(60)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_p:
                    paused = not paused

        if paused:
            # Draw pause screen
            pause_text = font.render("PAUSED - Press P to continue", True, (255, 255, 255))
            pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            win.fill((0, 0, 0))
            win.blit(pause_text, pause_rect)
            pygame.display.update()
            continue

        # Player controls (left paddle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            game.move_paddle(left=True, up=True)
        if keys[pygame.K_s]:
            game.move_paddle(left=True, up=False)

        # AI controls (right paddle) - TV1
        if ai_net:
            # Get game state for neural network
            ball_x = game.ball.x / WINDOW_WIDTH
            ball_y = game.ball.y / WINDOW_HEIGHT
            ball_vx = game.ball.x_vel / 10
            ball_vy = game.ball.y_vel / 10
            paddle_y = game.right_paddle.y / WINDOW_HEIGHT

            # Get ball and paddle positions
            ball_center_y = game.ball.y
            paddle_center_y = game.right_paddle.y + (game.right_paddle.HEIGHT * game.right_paddle.height_modifier / 2)

            # AI movement: always track ball position
            margin = 15  # Dead zone to avoid jittering
            if ball_center_y < paddle_center_y - margin:  # Ball above paddle
                game.move_paddle(left=False, up=True)
            elif ball_center_y > paddle_center_y + margin:  # Ball below paddle
                game.move_paddle(left=False, up=False)

        # Update power-ups (TV2 - Dũng)
        total_hits = game.left_hits + game.right_hits
        powerup_manager.update(total_hits)

        # Check power-up collisions
        collected = powerup_manager.check_collisions(
            game.ball.x, game.ball.y, game.ball.RADIUS
        )
        if collected:
            effects.add_hit_effect(game.ball.x, game.ball.y, color=(255, 255, 0))

        # Apply modifiers
        modifiers = powerup_manager.get_modifiers()
        game.left_paddle.apply_height_modifier(modifiers['paddle_height'])
        game.right_paddle.apply_height_modifier(modifiers['paddle_height'])
        game.ball.apply_speed_modifier(modifiers['ball_speed'])

        # Check scoring BEFORE game.loop (loop will reset ball)
        score_left_before = game.left_score
        score_right_before = game.right_score

        # Game loop
        game.loop()

        # Check if score changed and animate
        if game.right_score > score_right_before:
            effects.add_score_effect(WINDOW_WIDTH, game.ball.y)
            score_display.animate_score(right_scored=True)
        elif game.left_score > score_left_before:
            effects.add_score_effect(0, game.ball.y)
            score_display.animate_score(left_scored=True)

        # Update effects (TV4 - Bảo)
        effects.update()

        # Draw
        win.fill((0, 0, 0))

        # Apply screen shake
        shake_x, shake_y = effects.get_shake_offset()

        # Draw game (without score/hits - we'll draw them with ScoreDisplay)
        game.draw(draw_score=False, draw_hits=False)

        # Draw power-ups
        powerup_manager.draw(win)

        # Draw effects
        effects.draw(win)

        # Draw score with modern UI
        total_hits = game.left_hits + game.right_hits
        score_display.draw(win, game.left_score, game.right_score, total_hits)

        pygame.display.update()

        # Check game over
        if game.left_score >= 10 or game.right_score >= 10:
            if game.left_score >= 10:
                winner = "[VICTORY] HUMAN WINS!"
            else:
                winner = "[DEFEAT] AI DOMINANCE!"
            print(f"\n{winner}")
            print(f"Final Score: YOU {game.left_score} - {game.right_score} AI")

            # Show game over screen
            win.fill((0, 0, 0))
            winner_text = font.render(winner, True, (255, 255, 0))
            score_text = font.render(
                f"Final Score: {game.left_score} - {game.right_score}",
                True, (255, 255, 255)
            )

            win.blit(winner_text,
                    (WINDOW_WIDTH // 2 - winner_text.get_width() // 2,
                     WINDOW_HEIGHT // 2 - 50))
            win.blit(score_text,
                    (WINDOW_WIDTH // 2 - score_text.get_width() // 2,
                     WINDOW_HEIGHT // 2 + 20))

            pygame.display.update()
            pygame.time.delay(3000)
            running = False

    pygame.quit()
    print("[INFO] Game ended")


def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("NEAT PONG AI - Neural Evolution Gaming")
    print("="*60)
    print("Powered by NEAT Algorithm (NeuroEvolution)")
    print("Team Project:")
    print("  TV1 (Tri Hoang): AI Engine & Neural Networks")
    print("  TV2 (Dung): Game Physics & Mechanics")
    print("  TV3 (Trong Duc): Analytics & Training Dashboard")
    print("  TV4 (Bao): UI & Visual Effects")
    print("="*60 + "\n")

    while True:
        # Show menu (TV4 - Bảo)
        try:
            choice = show_menu(WINDOW_WIDTH, WINDOW_HEIGHT)
        except Exception as e:
            # Nếu menu UI lỗi trên Colab, dùng fallback text menu
            print("\n--- MENU ---")
            print("1. Train AI")
            print("2. Play vs Easy")
            print("3. Play vs Medium")
            print("4. Play vs Hard")
            print("5. Quit")
            c = input("Select: ")
            if c == '1': choice = 'train'
            elif c == '2': choice = 'play_easy'
            elif c == '3': choice = 'play_medium'
            elif c == '4': choice = 'play_hard'
            elif c == '5': choice = 'quit'
            else: choice = 'unknown'

        if choice == 'train':
            print("\n--- SELECT DIFFICULTY TO TRAIN ---")
            print("1. Easy (10 Generations)")
            print("2. Medium (25 Generations)")
            print("3. Hard (50 Generations)")
            d_choice = input("Enter selection (1-3): ")

            target = "medium"
            if d_choice == "1": target = "easy"
            elif d_choice == "3": target = "hard"

            train_ai(CONFIG_PATH, target_difficulty=target)

        elif choice == 'play_easy':
            play_vs_ai('easy')

        elif choice == 'play_medium':
            play_vs_ai('medium')

        elif choice == 'play_hard':
            play_vs_ai('hard')

        elif choice == 'quit':
            print("\n" + "="*50)
            print("Thanks for playing NEAT PONG AI!")
            break

        else:
            print(f"[!] Unknown choice: {choice}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Program interrupted by user")
    except Exception as e:
        print(f"\n[FATAL ERROR]: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit(0)
