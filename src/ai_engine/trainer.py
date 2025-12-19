"""
NEAT Trainer - TV1 (Trí Hoằng)
Training logic cho NEAT AI - Speed optimized
"""
import pygame
import neat
import time
from game_engine.game_manager import GameManager


class NEATTrainer:
    """
    Trainer cho NEAT neural networks
    Quản lý quá trình training và evaluation
    """
    
    def __init__(self, config, width=800, height=600, show_dashboard=False):
        """
        Khởi tạo trainer
        
        Args:
            config: NEAT config object
            width: Window width
            height: Window height
            show_dashboard: Hiển thị dashboard real-time
        """
        self.config = config
        self.width = width
        self.height = height
        self.show_dashboard = show_dashboard
        self.window = None
        
        # Always initialize pygame (needed for game logic even without display)
        pygame.init()
        
        # Create window only if showing dashboard
        if self.show_dashboard:
            self.window = pygame.display.set_mode((width, height))
            pygame.display.set_caption("NEAT Pong - Training")
        else:
            # Create invisible surface for headless training
            self.window = pygame.Surface((width, height))
    
    def train_ai(self, reporter=None, generations=None):
        """
        Train AI using NEAT algorithm
        
        Args:
            reporter: NEAT reporter (optional)
            generations: Number of generations (None = use config)
        
        Returns:
            Best genome after training
        """
        # Create population
        population = neat.Population(self.config)
        
        # Add reporters
        population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)
        
        if reporter:
            population.add_reporter(reporter)
        
        # Train
        if generations is None:
            generations = 50  # Default
        
        print(f"Training for {generations} generations...")
        
        # Run evolution
        winner = population.run(self._eval_genomes, generations)
        
        return winner
    
    def _eval_genomes(self, genomes, config):
        """
        NEAT evaluation function
        Called by population.run()
        
        Args:
            genomes: List of (genome_id, genome) tuples
            config: NEAT config
        """
        # Ensure window exists
        if self.window is None:
            self.window = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("NEAT Pong - Training")
        
        # Train each genome pair
        for i, (genome_id1, genome1) in enumerate(genomes):
            genome1.fitness = 0
            
            # Train against 2 opponents for maximum speed
            for genome_id2, genome2 in genomes[min(i+1, len(genomes)-1):i+2]:
                if genome2.fitness is None:
                    genome2.fitness = 0
                
                # Play game
                force_quit = self._train_pair(genome1, genome2)
                if force_quit:
                    return
    
    def _train_pair(self, genome1, genome2):
        """
        Train 2 genomes against each other
        
        Args:
            genome1: First genome
            genome2: Second genome
        
        Returns:
            bool: True if force quit
        """
        # Create networks
        net1 = neat.nn.FeedForwardNetwork.create(genome1, self.config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, self.config)
        
        # Create game
        game = GameManager(self.window, self.width, self.height)
        
        # Training config (extreme speed optimization)
        max_hits = 15  # Short games for fast training
        max_duration = 5  # Quick timeout
        start_time = time.time()
        
        # Only create clock if showing dashboard
        if self.show_dashboard:
            clock = pygame.time.Clock()
        
        run = True
        while run:
            # Only limit FPS if showing dashboard
            if self.show_dashboard:
                clock.tick(60)
            
            # Check quit events (only if showing dashboard)
            if self.show_dashboard:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return True
            else:
                # Clear events even when not showing to prevent queue buildup
                pygame.event.pump()
            
            # Game loop
            game.loop()
            
            # AI control
            self._move_ai_paddle(game, net1, genome1, game.left_paddle, True)
            self._move_ai_paddle(game, net2, genome2, game.right_paddle, False)
            
            # Draw only if dashboard enabled
            if self.show_dashboard:
                game.draw()
                pygame.display.update()
            
            # Check end conditions
            duration = time.time() - start_time
            total_hits = game.left_hits + game.right_hits
            if (game.left_score >= 1 or 
                game.right_score >= 1 or 
                total_hits >= max_hits or
                duration >= max_duration):  # Add timeout
                self._calculate_fitness(genome1, genome2, game, duration)
                break
        
        return False
    
    def _move_ai_paddle(self, game, net, genome, paddle, is_left):
        """
        Di chuyển paddle bởi AI
        
        Args:
            game: GameManager instance
            net: Neural network
            genome: NEAT genome
            paddle: Paddle object
            is_left: True nếu là paddle trái
        """
        # Get inputs (5 inputs as per config)
        ball_x = game.ball.x / self.width
        ball_y = game.ball.y / self.height
        ball_vx = game.ball.x_vel / 10
        ball_vy = game.ball.y_vel / 10
        paddle_y = paddle.y / self.height
        
        # AI decision
        output = net.activate((ball_x, ball_y, ball_vx, ball_vy, paddle_y))
        decision = output[0]
        
        # Execute action
        if decision > 0.5:  # Move up
            game.move_paddle(left=is_left, up=True)
        elif decision < -0.5:  # Move down
            game.move_paddle(left=is_left, up=False)
        # else: stay (do nothing)
    
    def _calculate_fitness(self, genome1, genome2, game, duration):
        """
        Tính fitness cho genomes
        
        Args:
            genome1: Genome 1
            genome2: Genome 2
            game: GameManager instance
            duration: Game duration in seconds
        """
        # Reward hits and duration
        genome1.fitness += game.left_hits * 2 + duration
        genome2.fitness += game.right_hits * 2 + duration
        
        # Bonus for winning
        if game.left_score > game.right_score:
            genome1.fitness += 10
        elif game.right_score > game.left_score:
            genome2.fitness += 10
