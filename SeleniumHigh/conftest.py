import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
from api.api_client import APIClient
import time


@pytest.fixture(scope="function")
def setup_browser():
    """Setup Chrome WebDriver"""
    try:
        # Create Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        
        # Try to find chromedriver in common locations
        chromedriver_paths = [
            "/usr/bin/chromedriver",
            "/usr/local/bin/chromedriver",
            "chromedriver",
            "../SeleniumMedium/drivers/chromedriver-linux64/chromedriver"
        ]
        
        service = None
        for path in chromedriver_paths:
            if os.path.exists(path):
                service = Service(executable_path=path)
                print(f"Using ChromeDriver at: {path}")
                break
        
        if service is None:
            # Fallback to system PATH
            service = Service()
            print("Using ChromeDriver from system PATH")
        
        # Create driver
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
        
        yield driver
        
    except Exception as e:
        print(f"Failed to setup browser: {e}")
        raise
    finally:
        if 'driver' in locals():
            driver.quit()


@pytest.fixture(scope="session")
def api_client():
    """Setup API client"""
    return APIClient()


@pytest.fixture(scope="session")
def test_user_data():
    """Test user data"""
    return {
        'first_name': 'Test',
        'last_name': 'User',
        'email': f'testuser_{int(time.time())}@example.com',
        'password': 'Test1234'
    } 