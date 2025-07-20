import os
import platform
from typing import Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from seleniumwire import webdriver as wire_webdriver

from .config_manager import config


class DriverFactory:
    """Factory class for creating WebDriver instances with different configurations"""
    
    def __init__(self):
        self.config = config
    
    def create_driver(self, browser: Optional[str] = None, 
                     headless: Optional[bool] = None,
                     mobile_emulation: Optional[bool] = None,
                     user_agent: Optional[str] = None,
                     window_size: Optional[str] = None,
                     enable_wire: bool = False) -> webdriver.Remote:
        """
        Create a WebDriver instance with specified configuration
        
        Args:
            browser: Browser type (chrome, firefox, safari, edge)
            headless: Run in headless mode
            mobile_emulation: Enable mobile emulation (Chrome only)
            user_agent: Custom user agent string
            window_size: Window size (e.g., "1920x1080")
            enable_wire: Enable selenium-wire for network capture
            
        Returns:
            WebDriver instance
        """
        browser = browser or self.config.get('browser.default', 'chrome')
        headless = headless if headless is not None else self.config.is_headless()
        mobile_emulation = mobile_emulation or self.config.get('browser.mobile_emulation', False)
        user_agent = user_agent or self.config.get('browser.user_agent', '')
        window_size = window_size or self.config.get('browser.window_size', '1920x1080')
        
        if enable_wire or self.config.get('performance.network_capture', False):
            return self._create_wire_driver(browser, headless, mobile_emulation, user_agent, window_size)
        else:
            return self._create_standard_driver(browser, headless, mobile_emulation, user_agent, window_size)
    
    def _create_standard_driver(self, browser: str, headless: bool, 
                               mobile_emulation: bool, user_agent: str, 
                               window_size: str) -> webdriver.Remote:
        """Create standard WebDriver instance"""
        
        if browser.lower() == 'chrome':
            return self._create_chrome_driver(headless, mobile_emulation, user_agent, window_size)
        elif browser.lower() == 'firefox':
            return self._create_firefox_driver(headless, user_agent, window_size)
        elif browser.lower() == 'edge':
            return self._create_edge_driver(headless, user_agent, window_size)
        elif browser.lower() == 'safari':
            return self._create_safari_driver(headless, user_agent, window_size)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    def _create_wire_driver(self, browser: str, headless: bool, 
                           mobile_emulation: bool, user_agent: str, 
                           window_size: str) -> webdriver.Remote:
        """Create selenium-wire WebDriver instance for network capture"""
        
        if browser.lower() == 'chrome':
            options = self._get_chrome_options(headless, mobile_emulation, user_agent)
            service = ChromeService(ChromeDriverManager().install())
            return wire_webdriver.Chrome(service=service, options=options)
        elif browser.lower() == 'firefox':
            options = self._get_firefox_options(headless, user_agent)
            service = FirefoxService(GeckoDriverManager().install())
            return wire_webdriver.Firefox(service=service, options=options)
        else:
            raise ValueError(f"Selenium-wire not supported for browser: {browser}")
    
    def _create_chrome_driver(self, headless: bool, mobile_emulation: bool, 
                             user_agent: str, window_size: str) -> webdriver.Chrome:
        """Create Chrome WebDriver"""
        options = self._get_chrome_options(headless, mobile_emulation, user_agent)
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        if window_size:
            width, height = window_size.split('x')
            driver.set_window_size(int(width), int(height))
        
        return driver
    
    def _create_firefox_driver(self, headless: bool, user_agent: str, 
                              window_size: str) -> webdriver.Firefox:
        """Create Firefox WebDriver"""
        options = self._get_firefox_options(headless, user_agent)
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
        if window_size:
            width, height = window_size.split('x')
            driver.set_window_size(int(width), int(height))
        
        return driver
    
    def _create_edge_driver(self, headless: bool, user_agent: str, 
                           window_size: str) -> webdriver.Edge:
        """Create Edge WebDriver"""
        options = self._get_edge_options(headless, user_agent)
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
        if window_size:
            width, height = window_size.split('x')
            driver.set_window_size(int(width), int(height))
        
        return driver
    
    def _create_safari_driver(self, headless: bool, user_agent: str, 
                             window_size: str) -> webdriver.Safari:
        """Create Safari WebDriver (macOS only)"""
        if platform.system() != 'Darwin':
            raise ValueError("Safari WebDriver is only supported on macOS")
        
        if headless:
            raise ValueError("Safari WebDriver does not support headless mode")
        
        options = self._get_safari_options(user_agent)
        driver = webdriver.Safari(options=options)
        
        if window_size:
            width, height = window_size.split('x')
            driver.set_window_size(int(width), int(height))
        
        return driver
    
    def _get_chrome_options(self, headless: bool, mobile_emulation: bool, 
                           user_agent: str) -> ChromeOptions:
        """Get Chrome options"""
        options = ChromeOptions()
        
        # Basic arguments
        chrome_args = self.config.get('browser.chrome.arguments', [])
        for arg in chrome_args:
            options.add_argument(arg)
        
        if headless:
            options.add_argument('--headless')
        
        if user_agent:
            options.add_argument(f'--user-agent={user_agent}')
        
        # Mobile emulation
        if mobile_emulation:
            mobile_emulation_config = {
                "deviceMetrics": {"width": 375, "height": 667, "pixelRatio": 2.0},
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
            }
            options.add_experimental_option("mobileEmulation", mobile_emulation_config)
        
        # Experimental options
        experimental_options = self.config.get('browser.chrome.experimental_options', {})
        for key, value in experimental_options.items():
            options.add_experimental_option(key, value)
        
        # Preferences
        prefs = self.config.get('browser.chrome.prefs', {})
        if prefs:
            options.add_experimental_option("prefs", prefs)
        
        return options
    
    def _get_firefox_options(self, headless: bool, user_agent: str) -> FirefoxOptions:
        """Get Firefox options"""
        options = FirefoxOptions()
        
        # Basic arguments
        firefox_args = self.config.get('browser.firefox.arguments', [])
        for arg in firefox_args:
            options.add_argument(arg)
        
        if headless:
            options.add_argument('--headless')
        
        if user_agent:
            options.add_argument(f'--user-agent={user_agent}')
        
        # Preferences
        prefs = self.config.get('browser.firefox.preferences', {})
        for key, value in prefs.items():
            options.set_preference(key, value)
        
        return options
    
    def _get_edge_options(self, headless: bool, user_agent: str) -> EdgeOptions:
        """Get Edge options"""
        options = EdgeOptions()
        
        if headless:
            options.add_argument('--headless')
        
        if user_agent:
            options.add_argument(f'--user-agent={user_agent}')
        
        return options
    
    def _get_safari_options(self, user_agent: str) -> SafariOptions:
        """Get Safari options"""
        options = SafariOptions()
        
        if user_agent:
            # Safari doesn't support custom user agent via options
            # This would need to be set via JavaScript after driver creation
            pass
        
        return options
    
    def create_cloud_driver(self, cloud_provider: str, capabilities: Dict[str, Any]) -> webdriver.Remote:
        """Create WebDriver for cloud testing (BrowserStack, Sauce Labs, etc.)"""
        
        if cloud_provider.lower() == 'browserstack':
            return self._create_browserstack_driver(capabilities)
        elif cloud_provider.lower() == 'saucelabs':
            return self._create_saucelabs_driver(capabilities)
        else:
            raise ValueError(f"Unsupported cloud provider: {cloud_provider}")
    
    def _create_browserstack_driver(self, capabilities: Dict[str, Any]) -> webdriver.Remote:
        """Create BrowserStack WebDriver"""
        cloud_config = self.config.get_cloud_config()
        bs_config = cloud_config.get('browserstack', {})
        
        if not bs_config.get('enabled', False):
            raise ValueError("BrowserStack is not enabled in configuration")
        
        username = bs_config.get('username') or os.getenv('BROWSERSTACK_USERNAME')
        access_key = bs_config.get('access_key') or os.getenv('BROWSERSTACK_ACCESS_KEY')
        
        if not username or not access_key:
            raise ValueError("BrowserStack username and access_key are required")
        
        capabilities.update({
            'bstack:options': {
                'userName': username,
                'accessKey': access_key,
                'osVersion': capabilities.get('osVersion', '10'),
                'projectName': 'SeleniumHigh',
                'buildName': 'SeleniumHigh Build',
                'sessionName': capabilities.get('sessionName', 'Test Session')
            }
        })
        
        return webdriver.Remote(
            command_executor='https://hub-cloud.browserstack.com/wd/hub',
            desired_capabilities=capabilities
        )
    
    def _create_saucelabs_driver(self, capabilities: Dict[str, Any]) -> webdriver.Remote:
        """Create Sauce Labs WebDriver"""
        cloud_config = self.config.get_cloud_config()
        sl_config = cloud_config.get('saucelabs', {})
        
        if not sl_config.get('enabled', False):
            raise ValueError("Sauce Labs is not enabled in configuration")
        
        username = sl_config.get('username') or os.getenv('SAUCE_USERNAME')
        access_key = sl_config.get('access_key') or os.getenv('SAUCE_ACCESS_KEY')
        
        if not username or not access_key:
            raise ValueError("Sauce Labs username and access_key are required")
        
        capabilities.update({
            'username': username,
            'accessKey': access_key,
            'name': capabilities.get('name', 'SeleniumHigh Test')
        })
        
        return webdriver.Remote(
            command_executor=f'https://{username}:{access_key}@ondemand.saucelabs.com:443/wd/hub',
            desired_capabilities=capabilities
        )
    
    def create_mobile_driver(self, platform: str, device_name: str, 
                           platform_version: str, automation_name: str) -> webdriver.Remote:
        """Create mobile WebDriver for Appium"""
        mobile_config = self.config.get_mobile_config()
        
        capabilities = {
            'platformName': platform or mobile_config.get('platform_name', 'iOS'),
            'deviceName': device_name or mobile_config.get('device_name', 'iPhone 12'),
            'platformVersion': platform_version or mobile_config.get('platform_version', '15.0'),
            'automationName': automation_name or mobile_config.get('automation_name', 'XCUITest')
        }
        
        # Appium server URL (default local)
        appium_url = os.getenv('APPIUM_URL', 'http://localhost:4723/wd/hub')
        
        return webdriver.Remote(
            command_executor=appium_url,
            desired_capabilities=capabilities
        )


# Global driver factory instance
driver_factory = DriverFactory() 