import logging
import logging.handlers
import os
import sys
from datetime import datetime
from typing import Optional
from pathlib import Path

from core.config_manager import config


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    # Color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        # Add color to levelname
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        
        return super().format(record)


class TestLogger:
    """Advanced logger for test automation with multiple handlers"""
    
    def __init__(self, name: str, log_file: Optional[str] = None):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if self.logger.handlers:
            return
        
        # Get configuration
        log_config = config.get_logging_config()
        log_level = getattr(logging, log_config.get('level', 'INFO'))
        log_format = log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        max_size = log_config.get('max_size', '10MB')
        backup_count = log_config.get('backup_count', 5)
        
        # Convert max_size to bytes
        if isinstance(max_size, str):
            size_map = {'KB': 1024, 'MB': 1024**2, 'GB': 1024**3}
            for unit, multiplier in size_map.items():
                if max_size.upper().endswith(unit):
                    max_size = int(max_size[:-2]) * multiplier
                    break
            else:
                max_size = 10 * 1024**2  # Default to 10MB
        
        # Console handler with colors
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_formatter = ColoredFormatter(log_format)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=max_size,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(log_format)
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
        
        # Error file handler (separate file for errors)
        error_log_file = log_file.replace('.log', '_error.log') if log_file else None
        if error_log_file:
            error_handler = logging.handlers.RotatingFileHandler(
                error_log_file,
                maxBytes=max_size,
                backupCount=backup_count,
                encoding='utf-8'
            )
            error_handler.setLevel(logging.ERROR)
            error_formatter = logging.Formatter(log_format)
            error_handler.setFormatter(error_formatter)
            self.logger.addHandler(error_handler)
    
    def debug(self, message: str) -> None:
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message: str) -> None:
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message: str) -> None:
        """Log critical message"""
        self.logger.critical(message)
    
    def exception(self, message: str) -> None:
        """Log exception with traceback"""
        self.logger.exception(message)


class PerformanceLogger:
    """Specialized logger for performance metrics"""
    
    def __init__(self, log_file: Optional[str] = None):
        self.logger = logging.getLogger('performance')
        self.logger.setLevel(logging.INFO)
        
        if self.logger.handlers:
            return
        
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            handler = logging.FileHandler(log_file, encoding='utf-8')
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def log_performance(self, test_name: str, duration: float, memory_usage: Optional[float] = None) -> None:
        """Log performance metrics"""
        message = f"PERFORMANCE - {test_name}: Duration={duration:.2f}s"
        if memory_usage:
            message += f", Memory={memory_usage:.2f}MB"
        self.logger.info(message)
    
    def log_network_request(self, url: str, method: str, status_code: int, duration: float) -> None:
        """Log network request metrics"""
        message = f"NETWORK - {method} {url}: Status={status_code}, Duration={duration:.2f}s"
        self.logger.info(message)


class APILogger:
    """Specialized logger for API calls"""
    
    def __init__(self, log_file: Optional[str] = None):
        self.logger = logging.getLogger('api')
        self.logger.setLevel(logging.INFO)
        
        if self.logger.handlers:
            return
        
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            handler = logging.FileHandler(log_file, encoding='utf-8')
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def log_request(self, method: str, url: str, headers: dict, data: Optional[dict] = None) -> None:
        """Log API request"""
        message = f"API REQUEST - {method} {url}"
        if headers:
            message += f" | Headers: {headers}"
        if data:
            message += f" | Data: {data}"
        self.logger.info(message)
    
    def log_response(self, status_code: int, response_time: float, response_data: Optional[dict] = None) -> None:
        """Log API response"""
        message = f"API RESPONSE - Status: {status_code}, Time: {response_time:.2f}s"
        if response_data:
            message += f" | Data: {response_data}"
        self.logger.info(message)
    
    def log_error(self, error: str, url: str) -> None:
        """Log API error"""
        message = f"API ERROR - {error} | URL: {url}"
        self.logger.error(message)


# Global logger instances
_loggers = {}


def get_logger(name: str) -> TestLogger:
    """Get or create a logger instance"""
    if name not in _loggers:
        log_config = config.get_logging_config()
        log_file = log_config.get('file', 'logs/test.log')
        _loggers[name] = TestLogger(name, log_file)
    
    return _loggers[name]


def get_performance_logger() -> PerformanceLogger:
    """Get performance logger instance"""
    log_config = config.get_logging_config()
    log_file = log_config.get('file', 'logs/performance.log')
    return PerformanceLogger(log_file)


def get_api_logger() -> APILogger:
    """Get API logger instance"""
    log_config = config.get_logging_config()
    log_file = log_config.get('file', 'logs/api.log')
    return APILogger(log_file)


def setup_test_logging(test_name: str) -> TestLogger:
    """Setup logging for a specific test"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/{test_name}_{timestamp}.log"
    
    logger = TestLogger(test_name, log_file)
    logger.info(f"=== Test Started: {test_name} ===")
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info(f"Environment: {config.get_environment()}")
    logger.info(f"Browser: {config.get('browser.default')}")
    
    return logger


def log_test_result(test_name: str, result: str, duration: float, error: Optional[str] = None) -> None:
    """Log test result"""
    logger = get_logger('test_results')
    
    message = f"TEST RESULT - {test_name}: {result.upper()}, Duration: {duration:.2f}s"
    if error:
        message += f", Error: {error}"
    
    if result.lower() == 'passed':
        logger.info(message)
    elif result.lower() == 'failed':
        logger.error(message)
    else:
        logger.warning(message)


def log_screenshot_taken(screenshot_path: str, reason: str) -> None:
    """Log screenshot taken"""
    logger = get_logger('screenshots')
    logger.info(f"Screenshot taken: {screenshot_path} | Reason: {reason}")


def log_element_interaction(element_name: str, action: str, success: bool, error: Optional[str] = None) -> None:
    """Log element interaction"""
    logger = get_logger('element_interactions')
    
    message = f"ELEMENT - {element_name}: {action}"
    if success:
        logger.info(message)
    else:
        logger.error(f"{message} | Error: {error}")


def log_page_navigation(url: str, success: bool, duration: Optional[float] = None) -> None:
    """Log page navigation"""
    logger = get_logger('navigation')
    
    message = f"NAVIGATION - {url}"
    if duration:
        message += f" | Duration: {duration:.2f}s"
    
    if success:
        logger.info(message)
    else:
        logger.error(message)


def log_configuration() -> None:
    """Log current configuration"""
    logger = get_logger('configuration')
    
    logger.info("=== Configuration ===")
    logger.info(f"Environment: {config.get_environment()}")
    logger.info(f"Base URL: {config.get_base_url()}")
    logger.info(f"Browser: {config.get('browser.default')}")
    logger.info(f"Headless: {config.is_headless()}")
    logger.info(f"Timeout: {config.get_timeout()}s")
    logger.info(f"Parallel: {config.is_parallel_enabled()}")
    logger.info(f"Workers: {config.get_workers()}")
    logger.info("=====================") 