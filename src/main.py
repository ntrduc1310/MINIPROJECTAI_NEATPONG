"""
NEAT Pong - Main Entry Point
Tích hợp tất cả modules: Game Engine, AI Engine, Features, UI
Team: TV1 (Trí Hoằng), TV2 (Dũng), TV3 (Trọng Đức - Game Engine & Analytics), TV4 (Bảo)
"""
import pygame
import neat
import os
import sys

# Import game engine (TV2 - Dũng, TV3 - Trọng Đức)
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
    print("\n" + "─"*45)
    print(f" Training Mode: {target_difficulty.upper()} Difficulty")
    print("─"*45)

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
        print(f" > Config: Loaded successfully")
    except Exception as e:
        print(f" ! Error: Could not load config - {e}")
        return

    # Init analytics
    analytics = TrainingAnalytics()

    # Init trainer (no display for speed)
    trainer = NEATTrainer(
        config,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        show_dashboard=False
    )
    print(f" > Trainer: Ready")

    # Lấy số thế hệ cần train từ ModelManager
    model_manager = get_model_manager()
    generations = model_manager.get_training_generations(target_difficulty)

    # Add reporter
    reporter = NEATReporter(analytics)

    # Start training
    print(f"\n Starting evolution process...")
    print(f" Generations: {generations}")
    print(f" Population: {model_manager.get_training_generations(target_difficulty)}")
    print(" (Press ESC to interrupt)\n")

    try:
        # Train với số thế hệ cụ thể cho độ khó đó và difficulty-specific config
        best_genome = trainer.train_ai(reporter=reporter, generations=generations, difficulty=target_difficulty)

        if best_genome:
            print("\n" + "─"*45)
            print(" Training Complete!")
            print("─"*45)
            print(f" Best Fitness Score: {best_genome.fitness:.2f}")

            # Save the trained model
            model_manager.save_model(best_genome, config, target_difficulty)
            print(f" Model saved: {target_difficulty}_ai.pkl")

            # Show summary stats
            summary = analytics.get_summary()
            print(f"\n Results:")
            print(f"  • Total generations: {summary['total_generations']}")
            print(f"  • Best fitness: {summary['best_fitness']:.2f}")
            print(f"  • Time elapsed: {summary['total_time']:.1f}s")
            print(f"  • Logs saved to: logs/")

    except KeyboardInterrupt:
        print("\n\n Training stopped by user.")
    except Exception as e:
        print(f"\n ! Error during training: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "─"*45)
    input("Press Enter to return to menu...")


def play_vs_ai(difficulty="medium", fullscreen=False):
    """
    Chơi với AI

    Args:
        difficulty: 'easy', 'medium', 'hard'
        fullscreen: Enable fullscreen mode
    """
    print(f"\n Loading {difficulty.upper()} AI opponent...")

    # Load model
    model_manager = get_model_manager()
    result = model_manager.load_genome_and_config(difficulty)

    if result is None:
        print(f" ! Model not found: {difficulty}_ai.pkl")
        print(f"   Please train {difficulty} AI first.")
        input("\n Press Enter to continue...")
        return

    ai_genome, config = result
    
    # Setup AI controller
    from ai_engine.ai_controller import create_ai_controller
    ai_controller = create_ai_controller(ai_genome, config, difficulty, WINDOW_WIDTH, WINDOW_HEIGHT)
    print(f" AI Ready: {difficulty.upper()} difficulty loaded\n")

    # Initialize pygame
    pygame.init()
    
    # Create window with fullscreen if enabled
    if fullscreen:
        display_info = pygame.display.Info()
        win = pygame.display.set_mode((display_info.current_w, display_info.current_h), pygame.FULLSCREEN)
        window_width = display_info.current_w
        window_height = display_info.current_h
    else:
        win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        window_width = WINDOW_WIDTH
        window_height = WINDOW_HEIGHT
    
    pygame.display.set_caption(f"NEAT Pong - vs {difficulty.upper()} AI")
    clock = pygame.time.Clock()

    # Initialize game (TV2 - Dũng)
    game = GameManager(win, window_width, window_height)
    
    # Calculate scale factor for fullscreen
    scale_factor = window_width / WINDOW_WIDTH
    
    # Adjust game speed based on difficulty for better balance
    if difficulty == "easy":
        # Easy: Much slower ball, faster player paddle
        game.ball.MAX_VEL = 3.5 * scale_factor
        game.ball.x_vel *= 0.7 * scale_factor
        game.ball.y_vel *= 0.7 * scale_factor
        game.left_paddle.VEL = 6 * scale_factor  # Player faster
        game.right_paddle.VEL = 3 * scale_factor  # AI slower
    elif difficulty == "medium":
        # Medium: Balanced speed
        game.ball.MAX_VEL = 5 * scale_factor
        game.ball.x_vel *= scale_factor
        game.ball.y_vel *= scale_factor
        game.left_paddle.VEL = 5 * scale_factor
        game.right_paddle.VEL = 4 * scale_factor
    elif difficulty == "hard":
        # Hard: Fast ball, normal player paddle
        game.ball.MAX_VEL = 6.5 * scale_factor
        game.ball.x_vel *= scale_factor
        game.ball.y_vel *= scale_factor
        game.left_paddle.VEL = 5 * scale_factor
        game.right_paddle.VEL = 5 * scale_factor

    # Initialize features
    powerup_manager = PowerUpManager(window_width, window_height)
    predictor = BallPredictor(window_width, window_height, Paddle.WIDTH, Paddle.HEIGHT)

    # Initialize UI (TV4 - Bảo)
    effects = VisualEffects()
    score_display = ScoreDisplay(window_width, window_height)

    # Game loop
    running = True
    game_state = "waiting"  # waiting, playing, paused
    font = pygame.font.Font(None, 40)
    title_font = pygame.font.Font(None, 60)
    small_font = pygame.font.Font(None, 30)

    print(" Game Starting...")
    print("\n Controls:")
    print("  W / S - Move paddle")
    print("  P - Pause game")
    print("  ESC - Quit to menu")
    print("  ENTER - Start game\n")

    while running:
        clock.tick(60)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN and game_state == "waiting":
                    game_state = "playing"
                elif event.key == pygame.K_p and game_state == "playing":
                    game_state = "paused"
                elif event.key == pygame.K_p and game_state == "paused":
                    game_state = "playing"
                elif event.key == pygame.K_SPACE and game_state == "waiting":
                    game_state = "playing"

        # Handle game states
        if game_state == "waiting":
            # Draw waiting screen
            game.draw(draw_score=False, draw_hits=False)
            
            # Semi-transparent overlay
            overlay = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            win.blit(overlay, (0, 0))
            
            # Title
            title_text = title_font.render(f"VS {difficulty.upper()} AI", True, (0, 255, 255))
            title_rect = title_text.get_rect(center=(window_width // 2, window_height // 3))
            win.blit(title_text, title_rect)
            
            # Instructions box
            box_width = 400
            box_height = 200
            box_x = window_width // 2 - box_width // 2
            box_y = window_height // 2 - 50
            
            box_surf = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            pygame.draw.rect(box_surf, (30, 30, 50, 220), box_surf.get_rect(), border_radius=15)
            pygame.draw.rect(box_surf, (100, 200, 255), box_surf.get_rect(), 3, border_radius=15)
            win.blit(box_surf, (box_x, box_y))
            
            # Instructions
            instructions = [
                "Press ENTER or SPACE to Start",
                "",
                "Controls:",
                "W / S - Move Paddle",
                "P - Pause Game",
                "ESC - Quit to Menu"
            ]
            
            y_offset = box_y + 20
            for i, line in enumerate(instructions):
                if i == 0:
                    text = font.render(line, True, (255, 255, 100))
                elif line == "":
                    continue
                else:
                    text = small_font.render(line, True, (200, 220, 255))
                text_rect = text.get_rect(center=(window_width // 2, y_offset))
                win.blit(text, text_rect)
                y_offset += 30 if i == 0 else 25
            
            pygame.display.update()
            continue

        elif game_state == "paused":
            # Draw pause screen
            game.draw(draw_score=True, draw_hits=True)
            
            # Semi-transparent overlay
            overlay = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            win.blit(overlay, (0, 0))
            
            # Pause box
            box_width = 350
            box_height = 150
            box_x = window_width // 2 - box_width // 2
            box_y = window_height // 2 - box_height // 2
            
            box_surf = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            pygame.draw.rect(box_surf, (30, 30, 50, 230), box_surf.get_rect(), border_radius=15)
            pygame.draw.rect(box_surf, (255, 200, 100), box_surf.get_rect(), 3, border_radius=15)
            win.blit(box_surf, (box_x, box_y))
            
            # Pause text
            pause_title = title_font.render("PAUSED", True, (255, 255, 100))
            pause_rect = pause_title.get_rect(center=(window_width // 2, window_height // 2 - 30))
            win.blit(pause_title, pause_rect)
            
            # Instructions
            resume_text = small_font.render("Press P to Resume", True, (200, 220, 255))
            resume_rect = resume_text.get_rect(center=(window_width // 2, window_height // 2 + 20))
            win.blit(resume_text, resume_rect)
            
            quit_text = small_font.render("Press ESC to Quit", True, (200, 220, 255))
            quit_rect = quit_text.get_rect(center=(window_width // 2, window_height // 2 + 50))
            win.blit(quit_text, quit_rect)
            
            pygame.display.update()
            continue

        # Player controls (left paddle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            game.move_paddle(left=True, up=True)
        if keys[pygame.K_s]:
            game.move_paddle(left=True, up=False)

        # AI controls (right paddle) - TV1 with difficulty-based behavior
        if ai_controller:
            # Get AI action using controller
            action = ai_controller.get_action(
                game.ball.x, game.ball.y,
                game.ball.x_vel, game.ball.y_vel,
                game.right_paddle.x, game.right_paddle.y,
                game.ball.RADIUS
            )
            
            # Apply speed factor based on difficulty
            speed_factor = ai_controller.get_speed_factor()
            
            # Execute action
            if action == 1:  # Move up
                game.move_paddle(left=False, up=True)
                # Apply speed modifier for lower difficulties
                if speed_factor < 1.0:
                    game.right_paddle.y += (1 - speed_factor) * game.right_paddle.VEL
            elif action == 2:  # Move down
                game.move_paddle(left=False, up=False)
                # Apply speed modifier for lower difficulties
                if speed_factor < 1.0:
                    game.right_paddle.y -= (1 - speed_factor) * game.right_paddle.VEL
            # else: stay (action == 0)

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
                    (window_width // 2 - winner_text.get_width() // 2,
                     window_height // 2 - 50))
            win.blit(score_text,
                    (window_width // 2 - score_text.get_width() // 2,
                     window_height // 2 + 20))

            pygame.display.update()
            pygame.time.delay(3000)
            running = False

    pygame.quit()
    print("[INFO] Game ended")


def main():
    """Main entry point"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "─"*50)
    print("     NEAT PONG - AI Training System")
    print("─"*50)
    print("Project: Neural Network Game AI")
    print("Algorithm: NEAT (NeuroEvolution)")
    print("\nDevelopment Team:")
    print("  • AI/ML Engine")
    print("  • Game Physics")
    print("  • Analytics System")
    print("  • UI/Graphics")
    print("─"*50 + "\n")

    while True:
        # Show menu (TV4 - Bảo)
        try:
            choice, is_fullscreen = show_menu(WINDOW_WIDTH, WINDOW_HEIGHT)
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
            is_fullscreen = False

        if choice == 'train':
            print("\n--- SELECT DIFFICULTY TO TRAIN ---")
            print("1. Easy (30 Generations)")
            print("2. Medium (60 Generations)")
            print("3. Hard (90 Generations)")
            d_choice = input("Enter selection (1-3): ")

            target = "medium"
            if d_choice == "1": target = "easy"
            elif d_choice == "3": target = "hard"

            train_ai(CONFIG_PATH, target_difficulty=target)

        elif choice == 'play_easy':
            play_vs_ai('easy', is_fullscreen)

        elif choice == 'play_medium':
            play_vs_ai('medium', is_fullscreen)

        elif choice == 'play_hard':
            play_vs_ai('hard', is_fullscreen)

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
