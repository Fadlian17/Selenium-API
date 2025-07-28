import requests
import time


class APIClient:
    """Simple API client for automationexercise.com"""
    
    def __init__(self):
        self.base_url = "https://automationexercise.com/api"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'SeleniumHigh/1.0'
        })
    
    def get(self, endpoint, params=None):
        """Make GET request"""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=30)
            return response
        except requests.exceptions.RequestException as e:
            print(f"API GET request failed: {e}")
            raise
    
    def post(self, endpoint, json_data=None):
        """Make POST request"""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.post(url, json=json_data, timeout=30)
            return response
        except requests.exceptions.RequestException as e:
            print(f"API POST request failed: {e}")
            raise
    
    def assert_status_code(self, response, expected_code):
        """Assert response status code"""
        if isinstance(expected_code, list):
            assert response.status_code in expected_code, f"Expected status code {expected_code}, got {response.status_code}"
        else:
            assert response.status_code == expected_code, f"Expected status code {expected_code}, got {response.status_code}" 