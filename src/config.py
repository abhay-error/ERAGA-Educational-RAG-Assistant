import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
import logging

class Config:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self._setup_logging()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file and resolve environment variables."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
            
        with open(self.config_path, 'r') as file:
            config = yaml.safe_load(file)
            
        # Resolve environment variables
        config = self._resolve_env_vars(config)
        
        # Create necessary directories
        self._create_directories(config)
        
        return config
    
    def _resolve_env_vars(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively resolve environment variables in config values."""
        if isinstance(config, dict):
            for key, value in config.items():
                config[key] = self._resolve_env_vars(value)
        elif isinstance(config, str) and config.startswith("${") and config.endswith("}"):
            env_var = config[2:-1]
            return os.getenv(env_var, "")
        return config
    
    def _create_directories(self, config: Dict[str, Any]):
        """Create necessary directories specified in config."""
        paths = config.get('paths', {})
        for path_key, path_value in paths.items():
            Path(path_value).mkdir(parents=True, exist_ok=True)
    
    def _setup_logging(self):
        """Setup logging based on config."""
        log_config = self.config.get('logging', {})
        log_level = getattr(logging, log_config.get('level', 'INFO'))
        log_file = log_config.get('file', './logs/rag_assistant.log')
        
        # Create logs directory if it doesn't exist
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value by key (supports dot notation)."""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        return value
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration."""
        return self.config.get('llm', {})
    
    def get_vector_db_config(self) -> Dict[str, Any]:
        """Get vector database configuration."""
        return self.config.get('vector_db', {})
    
    def get_web_search_config(self) -> Dict[str, Any]:
        """Get web search configuration."""
        return self.config.get('web_search', {})
    
    def get_ui_config(self) -> Dict[str, Any]:
        """Get UI configuration."""
        return self.config.get('ui', {})
    
    def get_paths(self) -> Dict[str, str]:
        """Get paths configuration."""
        return self.config.get('paths', {})

# Global config instance
config = Config()
