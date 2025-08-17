import time
import requests
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple
from datetime import datetime


class APITestBase(ABC):
    """Base class for API tests with common functionality"""
    
    def __init__(self, base_url: str = "https://automationexercise.com/api"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SeleniumHigh-TestSuite/1.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        })
    
    def make_request(self, method: str, endpoint: str, **kwargs) -> Tuple[requests.Response, float]:
        """Make HTTP request and measure response time"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        start_time = time.time()
        
        try:
            response = self.session.request(method, url, **kwargs)
            response_time = time.time() - start_time
            return response, response_time
        except Exception as e:
            response_time = time.time() - start_time
            raise e
    
    def get(self, endpoint: str, **kwargs) -> Tuple[requests.Response, float]:
        """Make GET request"""
        return self.make_request('GET', endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> Tuple[requests.Response, float]:
        """Make POST request"""
        return self.make_request('POST', endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> Tuple[requests.Response, float]:
        """Make PUT request"""
        return self.make_request('PUT', endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> Tuple[requests.Response, float]:
        """Make DELETE request"""
        return self.make_request('DELETE', endpoint, **kwargs)
    
    def assert_status_code(self, response: requests.Response, expected_codes: Any) -> bool:
        """Assert response status code"""
        if isinstance(expected_codes, list):
            return response.status_code in expected_codes
        return response.status_code == expected_codes
    
    def assert_response_contains(self, response: requests.Response, expected_text: str) -> bool:
        """Assert response contains expected text"""
        return expected_text in response.text
    
    def assert_json_contains_key(self, response: requests.Response, key: str) -> bool:
        """Assert JSON response contains expected key"""
        try:
            data = response.json()
            return key in data
        except ValueError:
            return False
    
    def create_test_user(self) -> Dict[str, str]:
        """Create test user data with unique email"""
        timestamp = int(time.time())
        return {
            'name': 'Test User',
            'email': f'testuser_{timestamp}@example.com',
            'password': 'Test1234',
            'title': 'Mr',
            'birth_date': '15',
            'birth_month': '06',
            'birth_year': '1990',
            'firstname': 'Test',
            'lastname': 'User',
            'company': 'Test Company',
            'address1': '123 Test Street',
            'address2': 'Apt 4B',
            'country': 'United States',
            'zipcode': '12345',
            'state': 'Test State',
            'city': 'Test City',
            'mobile_number': '1234567890'
        }
    
    def cleanup_test_user(self, email: str, password: str) -> bool:
        """Clean up test user account"""
        try:
            delete_data = {'email': email, 'password': password}
            response, _ = self.delete('deleteAccount', data=delete_data)
            return response.status_code == 200
        except Exception:
            return False
    
    def wait_for_condition(self, condition_func, timeout: int = 10, interval: float = 0.5) -> bool:
        """Wait for a condition to be met"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if condition_func():
                return True
            time.sleep(interval)
        return False
    
    def retry_request(self, request_func, max_retries: int = 3, delay: float = 1.0):
        """Retry request with exponential backoff"""
        for attempt in range(max_retries):
            try:
                return request_func()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                time.sleep(delay * (2 ** attempt))
    
    def log_test_result(self, test_name: str, status: str, response_time: float, 
                       expected_code: Any, actual_code: Optional[int] = None, 
                       error_message: Optional[str] = None) -> Dict[str, Any]:
        """Log test result in standardized format"""
        return {
            "test_name": test_name,
            "status": status,
            "expected_code": expected_code,
            "actual_code": actual_code,
            "response_time": response_time,
            "error_message": error_message,
            "timestamp": datetime.now().isoformat()
        }
    
    @abstractmethod
    def run_test(self) -> Dict[str, Any]:
        """Run the test and return result"""
        pass


class TestResult:
    """Container for test results"""
    
    def __init__(self, test_name: str, status: str, response_time: float = 0.0):
        self.test_name = test_name
        self.status = status
        self.response_time = response_time
        self.expected_code = None
        self.actual_code = None
        self.error_message = None
        self.response_data = None
        self.timestamp = datetime.now()
    
    def set_response_info(self, expected_code: Any, actual_code: Optional[int] = None):
        """Set response information"""
        self.expected_code = expected_code
        self.actual_code = actual_code
    
    def set_error(self, error_message: str):
        """Set error information"""
        self.error_message = error_message
    
    def set_response_data(self, data: Dict[str, Any]):
        """Set response data"""
        self.response_data = data
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "test_name": self.test_name,
            "status": self.status,
            "response_time": self.response_time,
            "expected_code": self.expected_code,
            "actual_code": self.actual_code,
            "error_message": self.error_message,
            "response_data": self.response_data,
            "timestamp": self.timestamp.isoformat()
        } 