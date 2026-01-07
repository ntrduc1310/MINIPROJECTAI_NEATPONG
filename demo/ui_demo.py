"""
Demo UI/UX Improvements
Test các cải tiến giao diện mới
"""
import pygame
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.game_engine.game_manager import GameManager
from src.ui.visuals import VisualEffects

def main():
    """Demo các hiệu ứng UI/UX mới"""
    
    pygame.init()
    
    # Setup window
    WIDTH, HEIGHT = 800, 600
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("NEAT Pong - UI/UX Demo")
    
    clock = pygame.time.Clock()
    
    # Create game manager
    game = GameManager(win, WIDTH, HEIGHT)
    
    # Create visual effects
    effects = VisualEffects()
    
    # Demo state
    running = True
    frame = 0
    demo_stage = 0
    wait_frames = 0
    
    print("\n" + "="*50)
    print("🎨 NEAT PONG - UI/UX DEMO")
    print("="*50)
    print("\nDemo sẽ tự động chạy qua các tính năng:")
    print("1. Gradient background vàng-cam")
    print("2. Glow effects cho paddle & ball")
    print("3. Trail effect cho ball")
    print("4. Particle effects khi hit")
    print("5. Screen shake")
    print("6. Score display hiện đại")
    print("\nNhấn ESC để thoát\n")
    
    while running:
        clock.tick(60)
        frame += 1
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Demo stages
        if wait_frames > 0:
            wait_frames -= 1
        else:
            if demo_stage == 0:
                # Stage 1: Show gradient background
                if frame == 60:
                    print("✨ Stage 1: Gradient background vàng-cam đẹp mắt")
                    wait_frames = 180
                    demo_stage = 1
            
            elif demo_stage == 1:
                # Stage 2: Move ball to show trail
                if frame % 2 == 0:
                    game.ball.move()
                    effects.add_ball_position(game.ball.x, game.ball.y)
                
                if frame == 300:
                    print("🌊 Stage 2: Trail effect cho ball (vệt theo chuyển động)")
                    wait_frames = 180
                    demo_stage = 2
            
            elif demo_stage == 2:
                # Stage 3: Simulate hit with particles
                game.ball.move()
                effects.add_ball_position(game.ball.x, game.ball.y)
                
                collision = game.handle_collision()
                if collision:
                    effects.add_hit_effect(game.ball.x, game.ball.y)
                    print("💥 Stage 3: Particle effects khi đánh bóng!")
                    wait_frames = 120
                    demo_stage = 3
            
            elif demo_stage == 3:
                # Stage 4: Continue with effects
                game.ball.move()
                effects.add_ball_position(game.ball.x, game.ball.y)
                game.handle_collision()
                
                if frame == 600:
                    print("📳 Stage 4: Screen shake effect")
                    effects.screen_shake = 8
                    wait_frames = 60
                    demo_stage = 4
            
            elif demo_stage == 4:
                # Stage 5: Score demo
                game.ball.move()
                effects.add_ball_position(game.ball.x, game.ball.y)
                
                if game.ball.x < 0:
                    game.ball.reset()
                    game.right_score += 1
                    effects.add_score_effect(WIDTH // 2, HEIGHT // 2)
                    print("🏆 Stage 5: Flash effect khi ghi điểm")
                elif game.ball.x > WIDTH:
                    game.ball.reset()
                    game.left_score += 1
                    effects.add_score_effect(WIDTH // 2, HEIGHT // 2)
                    print("🏆 Stage 5: Flash effect khi ghi điểm")
                
                game.handle_collision()
                
                if frame > 900:
                    demo_stage = 5
            
            else:
                # Loop back
                game.ball.move()
                effects.add_ball_position(game.ball.x, game.ball.y)
                game.handle_collision()
        
        # Move paddles automatically for demo
        if game.left_paddle.y + game.left_paddle.HEIGHT // 2 < game.ball.y:
            game.move_paddle(left=True, up=False)
        else:
            game.move_paddle(left=True, up=True)
        
        if game.right_paddle.y + game.right_paddle.HEIGHT // 2 < game.ball.y:
            game.move_paddle(left=False, up=False)
        else:
            game.move_paddle(left=False, up=True)
        
        # Update effects
        effects.update()
        
        # Get shake offset
        shake_x, shake_y = effects.get_shake_offset()
        
        # Draw everything
        game.draw(draw_score=True, draw_hits=True)
        
        # Draw effects (trail & particles)
        effects.draw(win)
        
        # Apply shake by redrawing at offset (simple demo)
        if shake_x != 0 or shake_y != 0:
            # Note: In production, you'd offset the entire surface
            pass
        
        # Draw demo info
        font = pygame.font.Font(None, 24)
        info_text = font.render(f"Demo Stage: {demo_stage} | Frame: {frame} | FPS: {int(clock.get_fps())}", 
                               True, (50, 30, 20))
        info_bg = pygame.Surface((info_text.get_width() + 20, 30), pygame.SRCALPHA)
        info_bg.fill((255, 255, 255, 180))
        win.blit(info_bg, (10, HEIGHT - 40))
        win.blit(info_text, (20, HEIGHT - 35))
        
        pygame.display.flip()
    
    pygame.quit()
    print("\n✅ Demo hoàn thành! Game đã được nâng cấp thành công.")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
