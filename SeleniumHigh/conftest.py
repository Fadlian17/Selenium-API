import pytest
import time
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional, Generator
from pathlib import Path

from core.config_manager import config
from core.driver_factory import driver_factory
from utils.logger import get_logger, setup_test_logging, log_test_result
from api.api_client import APIClient


# Global test data
test_data = {}
test_results = []


@pytest.fixture(scope="session")
def test_session_data() -> Dict[str, Any]:
    """Session-level test data that persists across all tests"""
    return {
        'session_start': datetime.now().isoformat(),
        'environment': config.get_environment(),
        'browser': config.get('browser.default'),
        'base_url': config.get_base_url(),
        'test_count': 0,
        'passed_count': 0,
        'failed_count': 0,
        'skipped_count': 0
    }


@pytest.fixture(scope="session")
def api_client() -> APIClient:
    """API client for integration testing"""
    api_base_url = config.get('environment.api_base_url', '')
    return APIClient(base_url=api_base_url)


@pytest.fixture(scope="function")
def setup_browser(request) -> Generator:
    """Setup WebDriver with advanced configuration"""
    # Get test-specific configuration
    browser = getattr(request, 'param', None) or config.get('browser.default')
    headless = getattr(request, 'param', None) or config.is_headless()
    mobile_emulation = getattr(request, 'param', None) or config.get('browser.mobile_emulation', False)
    user_agent = getattr(request, 'param', None) or config.get('browser.user_agent', '')
    window_size = getattr(request, 'param', None) or config.get('browser.window_size', '1920x1080')
    enable_wire = getattr(request, 'param', None) or config.get('performance.network_capture', False)
    
    # Setup test logging
    test_name = request.node.name
    logger = setup_test_logging(test_name)
    
    # Create driver
    driver = None
    try:
        logger.info(f"Creating {browser} driver...")
        driver = driver_factory.create_driver(
            browser=browser,
            headless=headless,
            mobile_emulation=mobile_emulation,
            user_agent=user_agent,
            window_size=window_size,
            enable_wire=enable_wire
        )
        
        # Navigate to base URL
        base_url = config.get_base_url()
        if base_url:
            driver.get(base_url)
            logger.info(f"Navigated to: {base_url}")
        
        # Set implicit wait
        driver.implicitly_wait(config.get('environment.implicit_wait', 10))
        
        # Store driver in request for cleanup
        request.driver = driver
        request.logger = logger
        
        logger.info("Browser setup completed successfully")
        yield driver
        
    except Exception as e:
        if logger:
            logger.error(f"Failed to setup browser: {str(e)}")
        raise
    
    finally:
        if driver:
            try:
                driver.quit()
                if logger:
                    logger.info("Browser closed successfully")
            except Exception as e:
                if logger:
                    logger.error(f"Error closing browser: {str(e)}")


@pytest.fixture(scope="function")
def setup_browser_chrome(request) -> Generator:
    """Setup Chrome WebDriver"""
    request.param = 'chrome'
    yield from setup_browser(request)


@pytest.fixture(scope="function")
def setup_browser_firefox(request) -> Generator:
    """Setup Firefox WebDriver"""
    request.param = 'firefox'
    yield from setup_browser(request)


@pytest.fixture(scope="function")
def setup_browser_edge(request) -> Generator:
    """Setup Edge WebDriver"""
    request.param = 'edge'
    yield from setup_browser(request)


@pytest.fixture(scope="function")
def setup_browser_headless(request) -> Generator:
    """Setup headless WebDriver"""
    request.param = True  # headless=True
    yield from setup_browser(request)


@pytest.fixture(scope="function")
def setup_browser_mobile(request) -> Generator:
    """Setup mobile emulation WebDriver"""
    request.param = True  # mobile_emulation=True
    yield from setup_browser(request)


@pytest.fixture(scope="function")
def test_data_manager() -> Dict[str, Any]:
    """Test data manager for data-driven testing"""
    return {
        'data': {},
        'variables': {},
        'cleanup_tasks': []
    }


@pytest.fixture(scope="function")
def performance_monitor() -> Dict[str, Any]:
    """Performance monitoring fixture"""
    return {
        'start_time': None,
        'end_time': None,
        'memory_usage': [],
        'network_requests': [],
        'page_load_times': []
    }


@pytest.fixture(scope="function")
def screenshot_manager(setup_browser) -> Any:
    """Screenshot manager fixture"""
    from utils.screenshot import ScreenshotManager
    return ScreenshotManager(setup_browser)


@pytest.fixture(scope="function")
def visual_testing_manager(screenshot_manager) -> Dict[str, Any]:
    """Visual testing manager fixture"""
    return {
        'screenshot_manager': screenshot_manager,
        'baselines': {},
        'comparisons': []
    }


@pytest.fixture(scope="session")
def test_environment() -> Dict[str, Any]:
    """Test environment configuration"""
    return {
        'name': config.get_environment(),
        'base_url': config.get_base_url(),
        'api_base_url': config.get('environment.api_base_url', ''),
        'timeout': config.get_timeout(),
        'implicit_wait': config.get('environment.implicit_wait', 10),
        'parallel': config.is_parallel_enabled(),
        'workers': config.get_workers()
    }


@pytest.fixture(scope="function")
def test_context(request, test_data_manager, performance_monitor) -> Dict[str, Any]:
    """Test context with all necessary components"""
    return {
        'test_name': request.node.name,
        'test_data': test_data_manager,
        'performance': performance_monitor,
        'start_time': time.time(),
        'screenshots': [],
        'logs': []
    }


# Pytest hooks
def pytest_configure(config):
    """Configure pytest with custom options"""
    # Add custom markers
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "e2e: marks tests as end-to-end tests"
    )
    config.addinivalue_line(
        "markers", "visual: marks tests as visual regression tests"
    )
    config.addinivalue_line(
        "markers", "api: marks tests as API tests"
    )
    config.addinivalue_line(
        "markers", "mobile: marks tests as mobile tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )
    
    # Log configuration
    logger = get_logger('pytest_configure')
    logger.info("Pytest configuration completed")


def pytest_sessionstart(session):
    """Called at the start of the test session"""
    logger = get_logger('pytest_session')
    logger.info("=== Test Session Started ===")
    logger.info(f"Session ID: {session.testscollected}")
    logger.info(f"Environment: {config.get_environment()}")
    logger.info(f"Base URL: {config.get_base_url()}")
    logger.info(f"Browser: {config.get('browser.default')}")
    logger.info(f"Parallel: {config.is_parallel_enabled()}")
    logger.info(f"Workers: {config.get_workers()}")


def pytest_sessionfinish(session, exitstatus):
    """Called at the end of the test session"""
    logger = get_logger('pytest_session')
    logger.info("=== Test Session Finished ===")
    logger.info(f"Exit Status: {exitstatus}")
    logger.info(f"Tests Collected: {session.testscollected}")
    logger.info(f"Tests Run: {len(session.testscollected)}")
    
    # Generate session report
    generate_session_report(session, exitstatus)


def pytest_runtest_setup(item):
    """Called before each test"""
    logger = get_logger('pytest_runtest')
    logger.info(f"Setting up test: {item.name}")
    
    # Check for test data file
    test_data_file = f"data/{item.name}.json"
    if os.path.exists(test_data_file):
        with open(test_data_file, 'r') as f:
            test_data[item.name] = json.load(f)
        logger.info(f"Loaded test data from: {test_data_file}")


def pytest_runtest_teardown(item, nextitem):
    """Called after each test"""
    logger = get_logger('pytest_runtest')
    logger.info(f"Tearing down test: {item.name}")
    
    # Clean up test data
    if item.name in test_data:
        del test_data[item.name]


def pytest_runtest_logstart(nodeid, location):
    """Called when a test starts running"""
    logger = get_logger('pytest_runtest')
    logger.info(f"Starting test: {nodeid}")


def pytest_runtest_logfinish(nodeid, location):
    """Called when a test finishes running"""
    logger = get_logger('pytest_runtest')
    logger.info(f"Finished test: {nodeid}")


def pytest_runtest_logreport(report):
    """Called for each test report"""
    logger = get_logger('pytest_runtest')
    
    if report.when == 'call':
        # Test execution completed
        duration = report.duration
        outcome = report.outcome
        
        logger.info(f"Test {report.nodeid} {outcome} in {duration:.2f}s")
        
        # Log test result
        log_test_result(report.nodeid, outcome, duration, str(report.longrepr) if report.longrepr else None)
        
        # Store result for session report
        test_results.append({
            'name': report.nodeid,
            'outcome': outcome,
            'duration': duration,
            'error': str(report.longrepr) if report.longrepr else None,
            'timestamp': datetime.now().isoformat()
        })
        
        # Take screenshot on failure
        if outcome == 'failed' and hasattr(report, 'driver'):
            try:
                from utils.screenshot import ScreenshotManager
                screenshot_manager = ScreenshotManager(report.driver)
                screenshot_path = screenshot_manager.take_screenshot(f"failed_{report.nodeid}")
                logger.info(f"Screenshot taken on failure: {screenshot_path}")
            except Exception as e:
                logger.error(f"Failed to take screenshot: {str(e)}")


def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    logger = get_logger('pytest_collection')
    logger.info(f"Collected {len(items)} tests")
    
    # Add markers based on test names
    for item in items:
        if 'test_api_' in item.name:
            item.add_marker(pytest.mark.api)
        if 'test_e2e_' in item.name:
            item.add_marker(pytest.mark.e2e)
        if 'test_visual_' in item.name:
            item.add_marker(pytest.mark.visual)
        if 'test_mobile_' in item.name:
            item.add_marker(pytest.mark.mobile)
        if 'test_performance_' in item.name:
            item.add_marker(pytest.mark.performance)


def pytest_generate_tests(metafunc):
    """Generate test parameters for data-driven testing"""
    # Check if test function has data parameter
    if 'test_data' in metafunc.fixturenames:
        # Load test data from file
        test_name = metafunc.function.__name__
        data_file = f"data/{test_name}.json"
        
        if os.path.exists(data_file):
            with open(data_file, 'r') as f:
                data = json.load(f)
            
            # Generate test cases
            test_cases = []
            for case in data.get('test_cases', []):
                test_cases.append(case)
            
            metafunc.parametrize('test_data', test_cases)


def generate_session_report(session, exitstatus):
    """Generate comprehensive session report"""
    logger = get_logger('pytest_session')
    
    # Calculate statistics
    total_tests = len(test_results)
    passed_tests = len([r for r in test_results if r['outcome'] == 'passed'])
    failed_tests = len([r for r in test_results if r['outcome'] == 'failed'])
    skipped_tests = len([r for r in test_results if r['outcome'] == 'skipped'])
    
    total_duration = sum(r['duration'] for r in test_results)
    avg_duration = total_duration / total_tests if total_tests > 0 else 0
    
    # Create report data
    report_data = {
        'session_info': {
            'start_time': datetime.now().isoformat(),
            'exit_status': str(exitstatus),
            'environment': config.get_environment(),
            'browser': config.get('browser.default'),
            'parallel': config.is_parallel_enabled(),
            'workers': config.get_workers()
        },
        'statistics': {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'skipped_tests': skipped_tests,
            'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            'total_duration': total_duration,
            'average_duration': avg_duration
        },
        'test_results': test_results
    }
    
    # Save report to file
    report_path = Path('reports') / f"session_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    logger.info(f"Session report saved: {report_path}")
    
    # Log summary
    logger.info("=== Session Summary ===")
    logger.info(f"Total Tests: {total_tests}")
    logger.info(f"Passed: {passed_tests}")
    logger.info(f"Failed: {failed_tests}")
    logger.info(f"Skipped: {skipped_tests}")
    logger.info(f"Success Rate: {report_data['statistics']['success_rate']:.1f}%")
    logger.info(f"Total Duration: {total_duration:.2f}s")
    logger.info(f"Average Duration: {avg_duration:.2f}s")


# Custom fixtures for specific testing scenarios
@pytest.fixture
def authenticated_browser(setup_browser, api_client):
    """Browser with authentication setup"""
    # This would handle login/authentication setup
    # For now, just return the browser
    yield setup_browser


@pytest.fixture
def database_connection():
    """Database connection for data validation"""
    # This would setup database connection
    # For now, return None
    yield None


@pytest.fixture
def mock_server():
    """Mock server for API testing"""
    # This would setup a mock server
    # For now, return None
    yield None


@pytest.fixture
def test_user_data():
    """Test user data for authentication"""
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    }


@pytest.fixture
def admin_user_data():
    """Admin user data for privileged operations"""
    return {
        'username': 'admin',
        'email': 'admin@example.com',
        'password': 'adminpass123'
    } 