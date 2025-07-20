"""
Core module for SeleniumHigh framework
Contains essential components for the testing framework
"""

from .config_manager import ConfigManager, config
from .driver_factory import DriverFactory, driver_factory

__all__ = [
    'ConfigManager',
    'config',
    'DriverFactory', 
    'driver_factory'
] 