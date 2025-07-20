#!/usr/bin/env python3
"""
Setup script for SeleniumHigh framework
Automates the initial setup and configuration
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def create_directories():
    """Create necessary directories for the project"""
    directories = [
        'logs',
        'reports',
        'screenshots',
        'screenshots/baseline',
        'screenshots/comparison',
        'screenshots/success',
        'screenshots/failed',
        'screenshots/visual',
        'data',
        'drivers',
        'config'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")


def copy_config_file():
    """Copy example config to actual config file"""
    example_config = Path("config/config.example.yaml")
    actual_config = Path("config/config.yaml")
    
    if not actual_config.exists() and example_config.exists():
        shutil.copy2(example_config, actual_config)
        print("✅ Copied config.example.yaml to config.yaml")
        print("⚠️  Please edit config.yaml with your specific settings")
    elif actual_config.exists():
        print("ℹ️  config.yaml already exists")
    else:
        print("❌ config.example.yaml not found")


def install_dependencies():
    """Install Python dependencies"""
    requirements_file = Path("requirements.txt")
    
    if requirements_file.exists():
        print("📦 Installing Python dependencies...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                         check=True, capture_output=True, text=True)
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            print("Please install manually: pip install -r requirements.txt")
    else:
        print("❌ requirements.txt not found")


def download_webdrivers():
    """Download WebDriver executables"""
    print("🌐 Downloading WebDrivers...")
    
    try:
        # This would use webdriver-manager to download drivers
        # For now, just create a placeholder
        drivers_dir = Path("drivers")
        drivers_dir.mkdir(exist_ok=True)
        
        # Create placeholder files
        (drivers_dir / "chromedriver").touch()
        (drivers_dir / "geckodriver").touch()
        (drivers_dir / "msedgedriver").touch()
        
        print("✅ WebDriver placeholders created")
        print("⚠️  Please download actual WebDriver executables or use webdriver-manager")
        
    except Exception as e:
        print(f"❌ Failed to setup WebDrivers: {e}")


def create_sample_tests():
    """Create sample test files"""
    sample_tests = {
        "tests/test_sample.py": '''import pytest
from selenium.webdriver.common.by import By

class TestSample:
    """Sample test class"""
    
    @pytest.mark.smoke
    def test_sample_functionality(self, setup_browser):
        """Sample test method"""
        driver = setup_browser
        
        # Navigate to a page
        driver.get("https://example.com")
        
        # Verify page title
        assert "Example Domain" in driver.title
        
        # Take screenshot
        driver.save_screenshot("screenshots/sample_test.png")
        
        print("✅ Sample test completed successfully")
''',
        "tests/test_api_sample.py": '''import pytest
from api.api_client import APIClient

class TestAPISample:
    """Sample API test class"""
    
    @pytest.mark.api
    def test_api_endpoint(self, api_client):
        """Sample API test method"""
        # Test a public API endpoint
        response = api_client.get("https://jsonplaceholder.typicode.com/posts/1")
        
        # Verify response
        assert response.status_code == 200
        
        data = response.json()
        assert "id" in data
        assert "title" in data
        
        print("✅ Sample API test completed successfully")
'''
    }
    
    for file_path, content in sample_tests.items():
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not file_path.exists():
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"✅ Created sample test: {file_path}")
        else:
            print(f"ℹ️  Sample test already exists: {file_path}")


def create_ci_config():
    """Create CI/CD configuration files"""
    ci_configs = {
        ".github/workflows/test.yml": '''name: SeleniumHigh Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10"]
        browser: [chrome, firefox]
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Install browser drivers
      run: |
        sudo apt-get update
        sudo apt-get install -y chromium-browser firefox
    
    - name: Run tests
      env:
        SELENIUM_BROWSER: ${{ matrix.browser }}
        SELENIUM_HEADLESS: true
      run: |
        pytest tests/ -v --html=reports/test_report.html
    
    - name: Upload test results
      uses: actions/upload-artifact@v2
      with:
        name: test-results-${{ matrix.browser }}
        path: reports/
''',
        "Jenkinsfile": '''pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.9'
        SELENIUM_HEADLESS = 'true'
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'python -m pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Test') {
            parallel {
                stage('Chrome Tests') {
                    environment {
                        SELENIUM_BROWSER = 'chrome'
                    }
                    steps {
                        sh 'pytest tests/ -v --html=reports/chrome_report.html'
                    }
                }
                
                stage('Firefox Tests') {
                    environment {
                        SELENIUM_BROWSER = 'firefox'
                    }
                    steps {
                        sh 'pytest tests/ -v --html=reports/firefox_report.html'
                    }
                }
            }
        }
        
        stage('Report') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: '*.html',
                    reportName: 'Test Reports'
                ])
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'reports/**/*', fingerprint: true
        }
    }
}'''
    }
    
    for file_path, content in ci_configs.items():
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not file_path.exists():
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"✅ Created CI config: {file_path}")
        else:
            print(f"ℹ️  CI config already exists: {file_path}")


def create_docker_config():
    """Create Docker configuration"""
    docker_configs = {
        "Dockerfile": '''FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    wget \\
    gnupg \\
    unzip \\
    xvfb \\
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \\
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \\
    && apt-get update \\
    && apt-get install -y google-chrome-stable \\
    && rm -rf /var/lib/apt/lists/*

# Install Firefox
RUN apt-get update && apt-get install -y firefox-esr \\
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p logs reports screenshots data

# Set environment variables
ENV SELENIUM_HEADLESS=true
ENV SELENIUM_BROWSER=chrome

# Run tests
CMD ["pytest", "tests/", "-v", "--html=reports/test_report.html"]
''',
        "docker-compose.yml": '''version: '3.8'

services:
  selenium-hub:
    image: selenium/hub:4.1.0
    container_name: selenium-hub
    ports:
      - "4442:4442"
      - "4443:4443"
      - "4444:4444"

  chrome:
    image: selenium/node-chrome:4.1.0
    shm_size: 2gb
    depends_on:
      - selenium-hub
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443

  firefox:
    image: selenium/node-firefox:4.1.0
    shm_size: 2gb
    depends_on:
      - selenium-hub
    environment:
      - SE_EVENT_BUS_HOST=selenium-hub
      - SE_EVENT_BUS_PUBLISH_PORT=4442
      - SE_EVENT_BUS_SUBSCRIBE_PORT=4443

  tests:
    build: .
    depends_on:
      - selenium-hub
    environment:
      - SELENIUM_HUB_URL=http://selenium-hub:4444/wd/hub
    volumes:
      - ./reports:/app/reports
      - ./screenshots:/app/screenshots
      - ./logs:/app/logs
'''
    }
    
    for file_path, content in docker_configs.items():
        file_path = Path(file_path)
        
        if not file_path.exists():
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"✅ Created Docker config: {file_path}")
        else:
            print(f"ℹ️  Docker config already exists: {file_path}")


def main():
    """Main setup function"""
    print("🚀 Setting up SeleniumHigh Framework...")
    print("=" * 50)
    
    # Create directories
    create_directories()
    
    # Copy config file
    copy_config_file()
    
    # Install dependencies
    install_dependencies()
    
    # Download WebDrivers
    download_webdrivers()
    
    # Create sample tests
    create_sample_tests()
    
    # Create CI/CD configs
    create_ci_config()
    
    # Create Docker configs
    create_docker_config()
    
    print("=" * 50)
    print("✅ SeleniumHigh Framework setup completed!")
    print("\n📋 Next steps:")
    print("1. Edit config/config.yaml with your settings")
    print("2. Download WebDriver executables or use webdriver-manager")
    print("3. Run sample tests: pytest tests/test_sample.py -v")
    print("4. Check the README.md for more information")
    print("\n🎉 Happy testing!")


if __name__ == "__main__":
    main() 