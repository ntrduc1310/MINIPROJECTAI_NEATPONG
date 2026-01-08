"""
Model Manager - TV1 (Trí Hoằng)
Quản lý save/load AI models
"""
import pickle
import os
import neat


class ModelManager:
    """Quản lý AI models với 3 difficulty levels"""
    
    MODELS_DIR = "models"
    DIFFICULTY_CONFIGS = {
        'easy': {'generations': 30, 'filename': 'ai_easy.pkl'},
        'medium': {'generations': 60, 'filename': 'ai_medium.pkl'},
        'hard': {'generations': 90, 'filename': 'ai_hard.pkl'}
    }
    
    def __init__(self, models_dir=None):
        """
        Khởi tạo model manager
        
        Args:
            models_dir: Thư mục chứa models (None = dùng default)
        """
        if models_dir:
            self.MODELS_DIR = models_dir
        
        # Tạo thư mục nếu chưa có
        if not os.path.exists(self.MODELS_DIR):
            os.makedirs(self.MODELS_DIR)
    
    def save_model(self, genome, config=None, difficulty='medium'):
        """
        Save AI model
        
        Args:
            genome: NEAT genome
            config: NEAT config (optional, will be saved with genome)
            difficulty: 'easy', 'medium', hoặc 'hard'
        
        Raises:
            ValueError: Nếu difficulty không hợp lệ
        """
        if difficulty not in self.DIFFICULTY_CONFIGS:
            raise ValueError(
                f"Invalid difficulty '{difficulty}'. "
                f"Must be one of: {list(self.DIFFICULTY_CONFIGS.keys())}"
            )
        
        filename = self.DIFFICULTY_CONFIGS[difficulty]['filename']
        filepath = os.path.join(self.MODELS_DIR, filename)
        
        try:
            # Save both genome and config together
            data = {'genome': genome, 'config': config} if config else genome
            with open(filepath, 'wb') as f:
                pickle.dump(data, f)
            print(f" > Saved {difficulty} AI model")
        except Exception as e:
            print(f" ! Error saving: {e}")
            raise
    
    def load_model(self, difficulty='medium'):
        """
        Load AI model
        
        Args:
            difficulty: 'easy', 'medium', hoặc 'hard'
        
        Returns:
            NEAT genome hoặc None nếu không tìm thấy
        
        Raises:
            ValueError: Nếu difficulty không hợp lệ
        """
        if difficulty not in self.DIFFICULTY_CONFIGS:
            raise ValueError(
                f"Invalid difficulty '{difficulty}'. "
                f"Must be one of: {list(self.DIFFICULTY_CONFIGS.keys())}"
            )
        
        filename = self.DIFFICULTY_CONFIGS[difficulty]['filename']
        filepath = os.path.join(self.MODELS_DIR, filename)
        
        if not os.path.exists(filepath):
            print(f"⚠ Model not found: {filepath}")
            return None
        
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            
            # Handle both old (genome only) and new (dict) formats
            if isinstance(data, dict) and 'genome' in data:
                genome = data['genome']
            else:
                genome = data
            
            print(f" > Loaded {difficulty} model")
            return genome
        except Exception as e:
            print(f" ! Load error: {e}")
            return None
    
    def load_genome_and_config(self, difficulty='medium'):
        """
        Load genome and config WITHOUT creating network
        Used when you want to create network manually
        
        Args:
            difficulty: 'easy', 'medium', or 'hard'
            
        Returns:
            Tuple (genome, config) or None if not found
        """
        filename = self.DIFFICULTY_CONFIGS[difficulty]['filename']
        filepath = os.path.join(self.MODELS_DIR, filename)
        
        if not os.path.exists(filepath):
            print(f" ! Model not found: {filepath}")
            return None
        
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            
            # Handle new format (dict with genome and config)
            if isinstance(data, dict) and 'genome' in data and 'config' in data:
                genome = data['genome']
                config = data['config']
            else:
                # Old format - load config separately
                genome = data if not isinstance(data, dict) else data.get('genome', data)
                
                # Load config from main config file
                config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                          "config", "config-feedforward.txt")
                config = neat.Config(
                    neat.DefaultGenome,
                    neat.DefaultReproduction,
                    neat.DefaultSpeciesSet,
                    neat.DefaultStagnation,
                    config_path
                )
            
            return (genome, config)
        except Exception as e:
            print(f" ! Load error: {e}")
            return None
    
    def load_ai_network(self, difficulty='medium'):
        """
        Load model, config và tạo neural network
        
        Args:
            difficulty: 'easy', 'medium', hoặc 'hard'
        
        Returns:
            Tuple (network, config) hoặc None nếu không tìm thấy
        """
        # Load model file
        filename = self.DIFFICULTY_CONFIGS[difficulty]['filename']
        filepath = os.path.join(self.MODELS_DIR, filename)
        
        if not os.path.exists(filepath):
            print(f"⚠ Model not found: {filepath}")
            return None
        
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            
            # Handle new format (dict with genome and config)
            if isinstance(data, dict) and 'genome' in data and 'config' in data:
                genome = data['genome']
                config = data['config']
            else:
                # Old format - need to load config separately
                genome = data if not isinstance(data, dict) else data.get('genome', data)
                
                # Load config from main config file (go up from src/ai_engine to project root)
                config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                          "config", "config-feedforward.txt")
                config = neat.Config(
                    neat.DefaultGenome,
                    neat.DefaultReproduction,
                    neat.DefaultSpeciesSet,
                    neat.DefaultStagnation,
                    config_path
                )
        except Exception as e:
            print(f" ! Load error: {e}")
            import traceback
            traceback.print_exc()
            return None
        
        # Create network
        try:
            network = neat.nn.FeedForwardNetwork.create(genome, config)
            return (network, config)
        except Exception as e:
            print(f" ! Network error: {e}")
            return None
    
    def model_exists(self, difficulty):
        """Kiểm tra model có tồn tại không"""
        filename = self.DIFFICULTY_CONFIGS[difficulty]['filename']
        filepath = os.path.join(self.MODELS_DIR, filename)
        return os.path.exists(filepath)
    
    def list_available_models(self):
        """Liệt kê các models có sẵn"""
        available = []
        for difficulty in ['easy', 'medium', 'hard']:
            if self.model_exists(difficulty):
                available.append(difficulty)
        return available
    
    def get_training_generations(self, difficulty):
        """Lấy số generations khuyến nghị cho difficulty"""
        return self.DIFFICULTY_CONFIGS[difficulty]['generations']


# Global instance
_model_manager = None

def get_model_manager(models_dir=None):
    """
    Get singleton model manager instance
    
    Args:
        models_dir: Thư mục models (chỉ dùng lần đầu)
    
    Returns:
        ModelManager instance
    """
    global _model_manager
    if _model_manager is None:
        _model_manager = ModelManager(models_dir)
    return _model_manager
