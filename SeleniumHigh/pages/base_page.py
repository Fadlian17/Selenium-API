from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class BasePage:
    """Base page object with common web interactions"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
    
    def find_element(self, locator):
        """Find element by locator tuple (By, value)"""
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            self.take_screenshot("element_not_found")
            raise Exception(f"Element not found: {locator}")
    
    def enter_text(self, locator, text):
        """Enter text into element"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.clear()
            element.send_keys(text)
        except TimeoutException:
            self.take_screenshot("enter_text_failed")
            raise Exception(f"Failed to enter text in {locator}")
    
    def click(self, locator):
        """Click on element"""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except TimeoutException:
            self.take_screenshot("click_failed")
            raise Exception(f"Failed to click {locator}")
    
    def navigate_to(self, url):
        """Navigate to URL"""
        self.driver.get(url)
        time.sleep(2)  # Simple wait for page load
    
    def take_screenshot(self, name):
        """Take screenshot"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"Screenshot saved: {filename}")
    
    def wait_for_element_present(self, locator, timeout=10):
        """Wait for element to be present"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False 