# SeleniumHigh - Advanced E2E Testing Framework

## Overview
SeleniumHigh adalah framework testing yang advanced untuk melakukan E2E (End-to-End) testing dan modular testing dengan fitur-fitur multifungsi.

## Fitur Utama
- **Multi-Browser Support**: Chrome, Firefox, Safari, Edge
- **Parallel Execution**: Testing paralel dengan pytest-xdist
- **API Testing Integration**: Kombinasi UI dan API testing
- **Data-Driven Testing**: Testing dengan multiple data sets
- **Visual Testing**: Screenshot comparison dan visual regression
- **Performance Monitoring**: Network capture dan performance metrics
- **Cross-Platform**: Support untuk Windows, Linux, macOS
- **CI/CD Ready**: Integration dengan GitHub Actions, Jenkins, dll
- **Reporting**: HTML, JSON, XML reports dengan screenshots
- **Mobile Testing**: Responsive testing dan mobile emulation

## Struktur Project
```
SeleniumHigh/
├── config/                 # Konfigurasi environment
├── core/                   # Core framework components
├── pages/                  # Page Object Models
├── tests/                  # Test cases
├── data/                   # Test data dan fixtures
├── utils/                  # Utility functions
├── reports/                # Test reports
├── screenshots/            # Screenshots dan visual testing
├── logs/                   # Log files
├── drivers/                # WebDriver executables
├── api/                    # API testing modules
└── mobile/                 # Mobile testing modules
```

## Setup dan Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment
cp config/config.example.yaml config/config.yaml
# Edit config.yaml sesuai environment

# Run tests
pytest tests/ -v
```

## Usage Examples
```python
# E2E Test Example
def test_complete_user_journey(setup_browser):
    home_page = HomePage(setup_browser)
    login_page = LoginPage(setup_browser)
    
    # Complete user flow
    home_page.navigate_to_login()
    login_page.login("user@example.com", "password")
    assert home_page.is_user_logged_in()

# API + UI Integration Test
def test_api_ui_integration(setup_browser, api_client):
    # API call to create user
    user_data = api_client.create_user(test_data)
    
    # UI verification
    home_page = HomePage(setup_browser)
    home_page.login(user_data['email'], user_data['password'])
    assert home_page.is_user_logged_in()
```

## Configuration
Framework mendukung multiple environment:
- Development
- Staging  
- Production
- Local

## Reporting
- HTML Reports dengan screenshots
- JSON/XML untuk CI/CD integration
- Performance metrics
- API call logs
- Visual regression reports 