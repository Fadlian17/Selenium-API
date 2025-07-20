"""
Utility modules for SeleniumHigh framework
Contains helper functions and utilities for testing
"""

from .logger import (
    get_logger,
    get_performance_logger,
    get_api_logger,
    setup_test_logging,
    log_test_result,
    log_screenshot_taken,
    log_element_interaction,
    log_page_navigation,
    log_configuration
)

from .screenshot import ScreenshotManager

__all__ = [
    'get_logger',
    'get_performance_logger', 
    'get_api_logger',
    'setup_test_logging',
    'log_test_result',
    'log_screenshot_taken',
    'log_element_interaction',
    'log_page_navigation',
    'log_configuration',
    'ScreenshotManager'
] 