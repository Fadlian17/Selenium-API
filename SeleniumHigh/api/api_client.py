import time
import json
import requests
import httpx
from typing import Dict, Any, Optional, List, Union
from urllib.parse import urljoin
import jsonschema
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from core.config_manager import config
from utils.logger import get_api_logger


class APIClient:
    """Advanced API client for integration testing"""
    
    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        self.api_config = config.get_api_config()
        self.base_url = base_url or self.api_config.get('base_url', '')
        self.timeout = timeout or self.api_config.get('timeout', 30)
        self.retry_attempts = self.api_config.get('retry_attempts', 3)
        self.retry_delay = self.api_config.get('retry_delay', 1)
        self.verify_ssl = self.api_config.get('verify_ssl', True)
        
        # Default headers
        self.default_headers = self.api_config.get('headers', {
            'Content-Type': 'application/json',
            'User-Agent': 'SeleniumHigh/1.0'
        })
        
        # Session for connection pooling
        self.session = self._create_session()
        self.logger = get_api_logger()
        
        # Request/response history
        self.request_history: List[Dict[str, Any]] = []
        self.response_history: List[Dict[str, Any]] = []
    
    def _create_session(self) -> requests.Session:
        """Create requests session with retry strategy"""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=self.retry_attempts,
            backoff_factor=self.retry_delay,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set default headers
        session.headers.update(self.default_headers)
        
        return session
    
    def _log_request(self, method: str, url: str, headers: dict, data: Optional[dict] = None) -> None:
        """Log API request"""
        self.logger.log_request(method, url, headers, data)
        
        self.request_history.append({
            'method': method,
            'url': url,
            'headers': headers,
            'data': data,
            'timestamp': time.time()
        })
    
    def _log_response(self, status_code: int, response_time: float, response_data: Optional[dict] = None) -> None:
        """Log API response"""
        self.logger.log_response(status_code, response_time, response_data)
        
        self.response_history.append({
            'status_code': status_code,
            'response_time': response_time,
            'response_data': response_data,
            'timestamp': time.time()
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with logging and error handling"""
        url = urljoin(self.base_url, endpoint)
        start_time = time.time()
        
        # Prepare request data
        headers = kwargs.pop('headers', {})
        data = kwargs.pop('data', None)
        json_data = kwargs.pop('json', None)
        
        # Log request
        self._log_request(method, url, headers, json_data or data)
        
        try:
            # Make request
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                data=data,
                json=json_data,
                timeout=self.timeout,
                verify=self.verify_ssl,
                **kwargs
            )
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Parse response data
            response_data = None
            try:
                if response.headers.get('content-type', '').startswith('application/json'):
                    response_data = response.json()
            except json.JSONDecodeError:
                response_data = response.text
            
            # Log response
            self._log_response(response.status_code, response_time, response_data)
            
            return response
            
        except requests.exceptions.RequestException as e:
            self.logger.log_error(str(e), url)
            raise
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, 
            headers: Optional[Dict[str, str]] = None, **kwargs) -> requests.Response:
        """Make GET request"""
        return self._make_request('GET', endpoint, params=params, headers=headers, **kwargs)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, 
             json_data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, 
             **kwargs) -> requests.Response:
        """Make POST request"""
        return self._make_request('POST', endpoint, data=data, json=json_data, headers=headers, **kwargs)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, 
            json_data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, 
            **kwargs) -> requests.Response:
        """Make PUT request"""
        return self._make_request('PUT', endpoint, data=data, json=json_data, headers=headers, **kwargs)
    
    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None, 
              json_data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, 
              **kwargs) -> requests.Response:
        """Make PATCH request"""
        return self._make_request('PATCH', endpoint, data=data, json=json_data, headers=headers, **kwargs)
    
    def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None, **kwargs) -> requests.Response:
        """Make DELETE request"""
        return self._make_request('DELETE', endpoint, headers=headers, **kwargs)
    
    def head(self, endpoint: str, headers: Optional[Dict[str, str]] = None, **kwargs) -> requests.Response:
        """Make HEAD request"""
        return self._make_request('HEAD', endpoint, headers=headers, **kwargs)
    
    def options(self, endpoint: str, headers: Optional[Dict[str, str]] = None, **kwargs) -> requests.Response:
        """Make OPTIONS request"""
        return self._make_request('OPTIONS', endpoint, headers=headers, **kwargs)
    
    def validate_response_schema(self, response: requests.Response, schema: Dict[str, Any]) -> bool:
        """Validate response against JSON schema"""
        try:
            response_data = response.json()
            jsonschema.validate(instance=response_data, schema=schema)
            return True
        except jsonschema.ValidationError as e:
            self.logger.log_error(f"Schema validation failed: {str(e)}", response.url)
            return False
        except json.JSONDecodeError as e:
            self.logger.log_error(f"Invalid JSON response: {str(e)}", response.url)
            return False
    
    def assert_status_code(self, response: requests.Response, expected_status: Union[int, List[int]]) -> None:
        """Assert response status code"""
        if isinstance(expected_status, int):
            expected_status = [expected_status]
        
        if response.status_code not in expected_status:
            raise AssertionError(
                f"Expected status code {expected_status}, but got {response.status_code}. "
                f"Response: {response.text}"
            )
    
    def assert_response_contains(self, response: requests.Response, expected_data: Dict[str, Any]) -> None:
        """Assert response contains expected data"""
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            raise AssertionError("Response is not valid JSON")
        
        for key, value in expected_data.items():
            if key not in response_data:
                raise AssertionError(f"Response does not contain key: {key}")
            if response_data[key] != value:
                raise AssertionError(f"Expected {key}={value}, but got {key}={response_data[key]}")
    
    def assert_response_time(self, response: requests.Response, max_time: float) -> None:
        """Assert response time is within limit"""
        # This would need to be implemented with response timing
        pass
    
    def get_response_data(self, response: requests.Response) -> Dict[str, Any]:
        """Get response data as dictionary"""
        try:
            return response.json()
        except json.JSONDecodeError:
            return {'text': response.text}
    
    def set_auth_token(self, token: str, token_type: str = 'Bearer') -> None:
        """Set authentication token"""
        self.session.headers['Authorization'] = f"{token_type} {token}"
    
    def set_basic_auth(self, username: str, password: str) -> None:
        """Set basic authentication"""
        self.session.auth = (username, password)
    
    def clear_auth(self) -> None:
        """Clear authentication"""
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
        self.session.auth = None
    
    def add_header(self, key: str, value: str) -> None:
        """Add custom header"""
        self.session.headers[key] = value
    
    def remove_header(self, key: str) -> None:
        """Remove custom header"""
        if key in self.session.headers:
            del self.session.headers[key]
    
    def get_request_history(self) -> List[Dict[str, Any]]:
        """Get request history"""
        return self.request_history.copy()
    
    def get_response_history(self) -> List[Dict[str, Any]]:
        """Get response history"""
        return self.response_history.copy()
    
    def clear_history(self) -> None:
        """Clear request/response history"""
        self.request_history.clear()
        self.response_history.clear()
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get API performance statistics"""
        if not self.response_history:
            return {}
        
        response_times = [resp['response_time'] for resp in self.response_history]
        status_codes = [resp['status_code'] for resp in self.response_history]
        
        return {
            'total_requests': len(self.response_history),
            'average_response_time': sum(response_times) / len(response_times),
            'min_response_time': min(response_times),
            'max_response_time': max(response_times),
            'success_rate': len([code for code in status_codes if 200 <= code < 300]) / len(status_codes),
            'error_rate': len([code for code in status_codes if code >= 400]) / len(status_codes)
        }
    
    def health_check(self, endpoint: str = '/health') -> bool:
        """Perform health check"""
        try:
            response = self.get(endpoint)
            return response.status_code == 200
        except Exception:
            return False
    
    def close(self) -> None:
        """Close session"""
        self.session.close()


class AsyncAPIClient:
    """Asynchronous API client using httpx"""
    
    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        self.api_config = config.get_api_config()
        self.base_url = base_url or self.api_config.get('base_url', '')
        self.timeout = timeout or self.api_config.get('timeout', 30)
        self.verify_ssl = self.api_config.get('verify_ssl', True)
        
        # Default headers
        self.default_headers = self.api_config.get('headers', {
            'Content-Type': 'application/json',
            'User-Agent': 'SeleniumHigh/1.0'
        })
        
        self.logger = get_api_logger()
    
    async def _make_request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        """Make async HTTP request"""
        url = urljoin(self.base_url, endpoint)
        start_time = time.time()
        
        # Prepare request data
        headers = kwargs.pop('headers', {})
        headers.update(self.default_headers)
        
        # Log request
        self.logger.log_request(method, url, headers, kwargs.get('json'))
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout, verify=self.verify_ssl) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    **kwargs
                )
                
                # Calculate response time
                response_time = time.time() - start_time
                
                # Parse response data
                response_data = None
                try:
                    if response.headers.get('content-type', '').startswith('application/json'):
                        response_data = response.json()
                except json.JSONDecodeError:
                    response_data = response.text
                
                # Log response
                self.logger.log_response(response.status_code, response_time, response_data)
                
                return response
                
        except httpx.RequestError as e:
            self.logger.log_error(str(e), url)
            raise
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, 
                  headers: Optional[Dict[str, str]] = None, **kwargs) -> httpx.Response:
        """Make async GET request"""
        return await self._make_request('GET', endpoint, params=params, headers=headers, **kwargs)
    
    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, 
                   json_data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, 
                   **kwargs) -> httpx.Response:
        """Make async POST request"""
        return await self._make_request('POST', endpoint, data=data, json=json_data, headers=headers, **kwargs)
    
    async def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, 
                  json_data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, 
                  **kwargs) -> httpx.Response:
        """Make async PUT request"""
        return await self._make_request('PUT', endpoint, data=data, json=json_data, headers=headers, **kwargs)
    
    async def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None, **kwargs) -> httpx.Response:
        """Make async DELETE request"""
        return await self._make_request('DELETE', endpoint, headers=headers, **kwargs) 