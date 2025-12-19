"""
Training Analytics - TV3 (Trọng Đức)
Hệ thống phân tích và trực quan hóa training
"""
import pygame
import csv
import os
import time
from datetime import datetime
import neat


class TrainingAnalytics:
    """Ghi log và phân tích training"""
    
    def __init__(self, log_dir="logs"):
        """
        Khởi tạo analytics
        
        Args:
            log_dir: Thư mục chứa logs
        """
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        # Log file paths
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.generation_log = os.path.join(log_dir, f"generation_{timestamp}.csv")
        self.genome_log = os.path.join(log_dir, f"genome_{timestamp}.csv")
        
        # Initialize CSV files
        self._init_generation_log()
        self._init_genome_log()
        
        # Session stats
        self.start_time = time.time()
        self.total_generations = 0
        self.best_fitness_ever = 0
        self.generation_times = []
    
    def _init_generation_log(self):
        """Tạo CSV header cho generation log"""
        try:
            with open(self.generation_log, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Generation',
                    'BestFitness',
                    'AvgFitness',
                    'MinFitness',
                    'StdDev',
                    'SpeciesCount',
                    'Duration(s)',
                    'Timestamp'
                ])
            print(f"📊 Generation log: {self.generation_log}")
        except Exception as e:
            print(f"❌ Error creating generation log: {e}")
    
    def _init_genome_log(self):
        """Tạo CSV header cho genome log"""
        try:
            with open(self.genome_log, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Generation',
                    'GenomeID',
                    'Fitness',
                    'Nodes',
                    'Connections',
                    'Timestamp'
                ])
            print(f"📊 Genome log: {self.genome_log}")
        except Exception as e:
            print(f"❌ Error creating genome log: {e}")
    
    def log_generation(self, generation, population):
        """
        Log thông tin generation
        
        Args:
            generation: Generation number
            population: NEAT population object
        """
        try:
            # Calculate stats
            fitnesses = [g.fitness for g in population.values() if g.fitness is not None]
            
            if not fitnesses:
                return
            
            best_fitness = max(fitnesses)
            avg_fitness = sum(fitnesses) / len(fitnesses)
            min_fitness = min(fitnesses)
            
            # Standard deviation
            variance = sum((f - avg_fitness) ** 2 for f in fitnesses) / len(fitnesses)
            std_dev = variance ** 0.5
            
            # Species count
            species_count = len(population)
            
            # Duration
            duration = 0
            if self.generation_times:
                duration = self.generation_times[-1]
            
            # Update best
            if best_fitness > self.best_fitness_ever:
                self.best_fitness_ever = best_fitness
            
            # Write to CSV
            with open(self.generation_log, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    generation,
                    best_fitness,
                    avg_fitness,
                    min_fitness,
                    std_dev,
                    species_count,
                    duration,
                    datetime.now().isoformat()
                ])
            
            self.total_generations = generation
            
        except Exception as e:
            print(f"❌ Error logging generation: {e}")
    
    def log_genome(self, generation, genome_id, genome):
        """
        Log thông tin genome
        
        Args:
            generation: Generation number
            genome_id: ID của genome
            genome: NEAT genome object
        """
        try:
            fitness = genome.fitness if genome.fitness else 0
            nodes = len(genome.nodes)
            connections = len(genome.connections)
            
            with open(self.genome_log, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    generation,
                    genome_id,
                    fitness,
                    nodes,
                    connections,
                    datetime.now().isoformat()
                ])
        except Exception as e:
            print(f"❌ Error logging genome: {e}")
    
    def record_generation_time(self, duration):
        """Ghi lại thời gian training của generation"""
        self.generation_times.append(duration)
    
    def get_summary(self):
        """Lấy tóm tắt session"""
        total_time = time.time() - self.start_time
        avg_gen_time = sum(self.generation_times) / len(self.generation_times) if self.generation_times else 0
        
        return {
            'total_generations': self.total_generations,
            'best_fitness': self.best_fitness_ever,
            'total_time': total_time,
            'avg_gen_time': avg_gen_time,
            'generation_log': self.generation_log,
            'genome_log': self.genome_log
        }


class TrainingDashboard:
    """Hiển thị dashboard real-time khi training"""
    
    def __init__(self, width=800, height=600):
        """
        Khởi tạo dashboard
        
        Args:
            width, height: Kích thước window
        """
        self.width = width
        self.height = height
        self.font = None
        self.title_font = None
        
        # Stats
        self.current_generation = 0
        self.best_fitness = 0
        self.avg_fitness = 0
        self.species_count = 0
        
        # History (cho graphs)
        self.fitness_history = []
        self.avg_fitness_history = []
        self.max_history = 50
    
    def init_fonts(self):
        """Khởi tạo fonts (gọi sau pygame.init())"""
        try:
            self.font = pygame.font.Font(None, 30)
            self.title_font = pygame.font.Font(None, 40)
        except Exception as e:
            print(f"⚠️ Font init warning: {e}")
            self.font = pygame.font.Font(None, 30)
            self.title_font = pygame.font.Font(None, 40)
    
    def update(self, generation, population):
        """
        Update dashboard với stats mới
        
        Args:
            generation: Generation number
            population: Dict của genomes
        """
        self.current_generation = generation
        
        # Calculate stats
        fitnesses = [g.fitness for g in population.values() if g.fitness is not None]
        
        if fitnesses:
            self.best_fitness = max(fitnesses)
            self.avg_fitness = sum(fitnesses) / len(fitnesses)
            
            # Update history
            self.fitness_history.append(self.best_fitness)
            self.avg_fitness_history.append(self.avg_fitness)
            
            # Limit history length
            if len(self.fitness_history) > self.max_history:
                self.fitness_history = self.fitness_history[-self.max_history:]
            if len(self.avg_fitness_history) > self.max_history:
                self.avg_fitness_history = self.avg_fitness_history[-self.max_history:]
        
        self.species_count = len(population)
    
    def draw(self, win):
        """
        Vẽ dashboard
        
        Args:
            win: Pygame window
        """
        if not self.font:
            self.init_fonts()
        
        # Background overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        win.blit(overlay, (0, 0))
        
        # Title
        title = self.title_font.render("🎮 NEAT Training Dashboard", True, (0, 255, 255))
        win.blit(title, (self.width // 2 - title.get_width() // 2, 30))
        
        # Stats
        y_offset = 100
        stats = [
            f"Generation: {self.current_generation}",
            f"Best Fitness: {self.best_fitness:.2f}",
            f"Avg Fitness: {self.avg_fitness:.2f}",
            f"Species: {self.species_count}",
        ]
        
        for stat in stats:
            text = self.font.render(stat, True, (255, 255, 255))
            win.blit(text, (50, y_offset))
            y_offset += 40
        
        # Graph area
        if len(self.fitness_history) > 1:
            self._draw_graph(win)
        
        # Instructions
        instructions = self.font.render("Press ESC to stop training", True, (255, 200, 0))
        win.blit(instructions, (self.width // 2 - instructions.get_width() // 2, 
                               self.height - 50))
    
    def _draw_graph(self, win):
        """Vẽ graph fitness history"""
        graph_x = 50
        graph_y = 300
        graph_width = self.width - 100
        graph_height = 200
        
        # Border
        pygame.draw.rect(win, (100, 100, 100), 
                        (graph_x, graph_y, graph_width, graph_height), 2)
        
        # Title
        graph_title = self.font.render("Fitness History", True, (200, 200, 200))
        win.blit(graph_title, (graph_x, graph_y - 30))
        
        if not self.fitness_history:
            return
        
        # Scale data
        max_fitness = max(self.fitness_history) if self.fitness_history else 1
        min_fitness = min(self.fitness_history) if self.fitness_history else 0
        fitness_range = max_fitness - min_fitness if max_fitness != min_fitness else 1
        
        # Draw best fitness line
        if len(self.fitness_history) > 1:
            points = []
            for i, fitness in enumerate(self.fitness_history):
                x = graph_x + (i / max(len(self.fitness_history) - 1, 1)) * graph_width
                y = graph_y + graph_height - ((fitness - min_fitness) / fitness_range) * graph_height
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(win, (0, 255, 0), False, points, 2)
        
        # Draw avg fitness line
        if len(self.avg_fitness_history) > 1:
            points = []
            for i, fitness in enumerate(self.avg_fitness_history):
                x = graph_x + (i / max(len(self.avg_fitness_history) - 1, 1)) * graph_width
                y = graph_y + graph_height - ((fitness - min_fitness) / fitness_range) * graph_height
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(win, (0, 150, 255), False, points, 2)
        
        # Legend
        legend_y = graph_y + graph_height + 10
        pygame.draw.line(win, (0, 255, 0), (graph_x, legend_y), 
                        (graph_x + 30, legend_y), 2)
        legend_text = self.font.render("Best", True, (200, 200, 200))
        win.blit(legend_text, (graph_x + 40, legend_y - 10))
        
        pygame.draw.line(win, (0, 150, 255), (graph_x + 150, legend_y), 
                        (graph_x + 180, legend_y), 2)
        legend_text = self.font.render("Average", True, (200, 200, 200))
        win.blit(legend_text, (graph_x + 190, legend_y - 10))
    
    def reset(self):
        """Reset dashboard"""
        self.current_generation = 0
        self.best_fitness = 0
        self.avg_fitness = 0
        self.species_count = 0
        self.fitness_history.clear()
        self.avg_fitness_history.clear()


class NEATReporter(neat.reporting.BaseReporter):
    """NEAT reporter tích hợp với analytics"""
    
    def __init__(self, analytics):
        """
        Khởi tạo reporter
        
        Args:
            analytics: TrainingAnalytics instance
        """
        super().__init__()
        self.analytics = analytics
        self.generation_start_time = None
    
    def start_generation(self, generation):
        """Bắt đầu generation"""
        self.generation_start_time = time.time()
        print(f"\n🚀 Generation {generation} started")
    
    def end_generation(self, config, population, species_set):
        """Kết thúc generation"""
        if self.generation_start_time:
            duration = time.time() - self.generation_start_time
            self.analytics.record_generation_time(duration)
            print(f"⏱️  Generation completed in {duration:.2f}s")
    
    def post_evaluate(self, config, population, species, best_genome):
        """Sau khi evaluate"""
        # Log generation stats
        generation = self.analytics.total_generations + 1
        self.analytics.log_generation(generation, population)
        
        # Log individual genomes
        for genome_id, genome in population.items():
            self.analytics.log_genome(generation, genome_id, genome)
        
        # Print best
        if best_genome.fitness:
            print(f"🏆 Best fitness: {best_genome.fitness:.2f}")
    
    def found_solution(self, config, generation, best):
        """Tìm được solution"""
        print(f"\n🎉 Solution found at generation {generation}!")
        print(f"🏆 Best fitness: {best.fitness:.2f}")
