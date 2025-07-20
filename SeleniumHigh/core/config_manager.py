import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigManager:
    """Manages configuration for the SeleniumHigh framework"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self._validate_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        config_file = Path(self.config_path)
        
        if not config_file.exists():
            # Try to load from example file
            example_file = Path("config/config.example.yaml")
            if example_file.exists():
                print(f"⚠️  Config file not found. Using example config: {example_file}")
                config_file = example_file
            else:
                raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(config_file, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        # Override with environment variables
        config = self._override_with_env_vars(config)
        
        return config
    
    def _override_with_env_vars(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Override config values with environment variables"""
        env_mappings = {
            'SELENIUM_ENV': ('environment', 'name'),
            'SELENIUM_BASE_URL': ('environment', 'base_url'),
            'SELENIUM_BROWSER': ('browser', 'default'),
            'SELENIUM_HEADLESS': ('browser', 'headless'),
            'SELENIUM_TIMEOUT': ('environment', 'timeout'),
            'SELENIUM_WORKERS': ('parallel', 'workers'),
        }
        
        for env_var, config_path in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value is not None:
                # Navigate to nested config path
                current = config
                for key in config_path[:-1]:
                    current = current[key]
                
                # Convert string values to appropriate types
                if env_var == 'SELENIUM_HEADLESS':
                    current[config_path[-1]] = env_value.lower() == 'true'
                elif env_var == 'SELENIUM_TIMEOUT':
                    current[config_path[-1]] = int(env_value)
                elif env_var == 'SELENIUM_WORKERS':
                    current[config_path[-1]] = int(env_value)
                else:
                    current[config_path[-1]] = env_value
        
        return config
    
    def _validate_config(self):
        """Validate configuration structure"""
        required_sections = ['environment', 'browser', 'reporting', 'screenshots']
        
        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"Missing required configuration section: {section}")
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_environment(self) -> str:
        """Get current environment name"""
        return self.get('environment.name', 'development')
    
    def get_base_url(self) -> str:
        """Get base URL for testing"""
        return self.get('environment.base_url', 'http://localhost')
    
    def get_browser_config(self) -> Dict[str, Any]:
        """Get browser configuration"""
        return self.get('browser', {})
    
    def get_timeout(self) -> int:
        """Get default timeout value"""
        return self.get('environment.timeout', 30)
    
    def is_parallel_enabled(self) -> bool:
        """Check if parallel execution is enabled"""
        return self.get('parallel.enabled', False)
    
    def get_workers(self) -> int:
        """Get number of parallel workers"""
        return self.get('parallel.workers', 1)
    
    def is_headless(self) -> bool:
        """Check if headless mode is enabled"""
        return self.get('browser.headless', False)
    
    def get_screenshot_config(self) -> Dict[str, Any]:
        """Get screenshot configuration"""
        return self.get('screenshots', {})
    
    def get_reporting_config(self) -> Dict[str, Any]:
        """Get reporting configuration"""
        return self.get('reporting', {})
    
    def get_api_config(self) -> Dict[str, Any]:
        """Get API testing configuration"""
        return self.get('api', {})
    
    def get_performance_config(self) -> Dict[str, Any]:
        """Get performance monitoring configuration"""
        return self.get('performance', {})
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration"""
        return self.get('database', {})
    
    def get_cloud_config(self) -> Dict[str, Any]:
        """Get cloud testing configuration"""
        return self.get('cloud', {})
    
    def get_mobile_config(self) -> Dict[str, Any]:
        """Get mobile testing configuration"""
        return self.get('mobile', {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration"""
        return self.get('logging', {})
    
    def get_email_config(self) -> Dict[str, Any]:
        """Get email notification configuration"""
        return self.get('email', {})
    
    def get_slack_config(self) -> Dict[str, Any]:
        """Get Slack notification configuration"""
        return self.get('slack', {})
    
    def get_test_data_config(self) -> Dict[str, Any]:
        """Get test data configuration"""
        return self.get('test_data', {})
    
    def get_visual_testing_config(self) -> Dict[str, Any]:
        """Get visual testing configuration"""
        return self.get('visual_testing', {})
    
    def get_hooks_config(self) -> Dict[str, Any]:
        """Get custom hooks configuration"""
        return self.get('hooks', {})
    
    def update_config(self, updates: Dict[str, Any]):
        """Update configuration with new values"""
        def update_nested(d, u):
            for k, v in u.items():
                if isinstance(v, dict):
                    d[k] = update_nested(d.get(k, {}), v)
                else:
                    d[k] = v
            return d
        
        self.config = update_nested(self.config, updates)
    
    def save_config(self, path: Optional[str] = None):
        """Save current configuration to file"""
        save_path = path or self.config_path
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, 'w', encoding='utf-8') as file:
            yaml.dump(self.config, file, default_flow_style=False, indent=2)


# Global config instance
config = ConfigManager() 