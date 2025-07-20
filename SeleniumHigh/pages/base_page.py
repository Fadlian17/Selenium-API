import time
import os
from typing import Optional, List, Dict, Any, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

from core.config_manager import config
from utils.logger import get_logger
from utils.screenshot import ScreenshotManager


class BasePage:
    """Advanced base page class with comprehensive functionality"""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.get_timeout())
        self.logger = get_logger(__name__)
        self.screenshot_manager = ScreenshotManager(driver)
        self.actions = ActionChains(driver)
        
        # Performance tracking
        self.start_time = None
        self.end_time = None
    
    def navigate_to(self, url: str) -> None:
        """Navigate to a specific URL"""
        try:
            self.logger.info(f"Navigating to: {url}")
            self.driver.get(url)
            self._wait_for_page_load()
        except Exception as e:
            self.logger.error(f"Failed to navigate to {url}: {str(e)}")
            self.screenshot_manager.take_screenshot("navigation_error")
            raise
    
    def _wait_for_page_load(self) -> None:
        """Wait for page to fully load"""
        try:
            self.wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            self.logger.warning("Page load timeout")
    
    def find_element(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        """Find element with explicit wait"""
        wait_time = timeout or config.get_timeout()
        wait = WebDriverWait(self.driver, wait_time)
        
        try:
            element = wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {locator}")
            self.screenshot_manager.take_screenshot("element_not_found")
            raise
    
    def find_elements(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> List[WebElement]:
        """Find multiple elements with explicit wait"""
        wait_time = timeout or config.get_timeout()
        wait = WebDriverWait(self.driver, wait_time)
        
        try:
            elements = wait.until(EC.presence_of_all_elements_located(locator))
            return elements
        except TimeoutException:
            self.logger.error(f"Elements not found: {locator}")
            self.screenshot_manager.take_screenshot("elements_not_found")
            raise
    
    def wait_for_element_clickable(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        """Wait for element to be clickable"""
        wait_time = timeout or config.get_timeout()
        wait = WebDriverWait(self.driver, wait_time)
        
        try:
            element = wait.until(EC.element_to_be_clickable(locator))
            return element
        except TimeoutException:
            self.logger.error(f"Element not clickable: {locator}")
            self.screenshot_manager.take_screenshot("element_not_clickable")
            raise
    
    def wait_for_element_visible(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> WebElement:
        """Wait for element to be visible"""
        wait_time = timeout or config.get_timeout()
        wait = WebDriverWait(self.driver, wait_time)
        
        try:
            element = wait.until(EC.visibility_of_element_located(locator))
            return element
        except TimeoutException:
            self.logger.error(f"Element not visible: {locator}")
            self.screenshot_manager.take_screenshot("element_not_visible")
            raise
    
    def click(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> None:
        """Click element with retry mechanism"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                element = self.wait_for_element_clickable(locator, timeout)
                self.actions.move_to_element(element).click().perform()
                self.logger.info(f"Clicked element: {locator}")
                return
            except (StaleElementReferenceException, TimeoutException) as e:
                if attempt == max_retries - 1:
                    self.logger.error(f"Failed to click element after {max_retries} attempts: {locator}")
                    self.screenshot_manager.take_screenshot("click_failed")
                    raise
                self.logger.warning(f"Click attempt {attempt + 1} failed, retrying...")
                time.sleep(1)
    
    def click_js(self, locator: Tuple[str, str]) -> None:
        """Click element using JavaScript"""
        try:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].click();", element)
            self.logger.info(f"Clicked element using JS: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to click element using JS: {locator}")
            self.screenshot_manager.take_screenshot("js_click_failed")
            raise
    
    def enter_text(self, locator: Tuple[str, str], text: str, clear_first: bool = True) -> None:
        """Enter text into element"""
        try:
            element = self.wait_for_element_clickable(locator)
            if clear_first:
                element.clear()
            element.send_keys(text)
            self.logger.info(f"Entered text '{text}' into element: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to enter text into element: {locator}")
            self.screenshot_manager.take_screenshot("enter_text_failed")
            raise
    
    def get_text(self, locator: Tuple[str, str]) -> str:
        """Get text from element"""
        try:
            element = self.find_element(locator)
            text = element.text
            self.logger.info(f"Got text '{text}' from element: {locator}")
            return text
        except Exception as e:
            self.logger.error(f"Failed to get text from element: {locator}")
            self.screenshot_manager.take_screenshot("get_text_failed")
            raise
    
    def get_attribute(self, locator: Tuple[str, str], attribute: str) -> str:
        """Get attribute value from element"""
        try:
            element = self.find_element(locator)
            value = element.get_attribute(attribute)
            self.logger.info(f"Got attribute '{attribute}' = '{value}' from element: {locator}")
            return value
        except Exception as e:
            self.logger.error(f"Failed to get attribute from element: {locator}")
            self.screenshot_manager.take_screenshot("get_attribute_failed")
            raise
    
    def is_element_present(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """Check if element is present"""
        try:
            self.find_element(locator, timeout)
            return True
        except TimeoutException:
            return False
    
    def is_element_visible(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """Check if element is visible"""
        try:
            self.wait_for_element_visible(locator, timeout)
            return True
        except TimeoutException:
            return False
    
    def is_element_enabled(self, locator: Tuple[str, str]) -> bool:
        """Check if element is enabled"""
        try:
            element = self.find_element(locator)
            return element.is_enabled()
        except Exception:
            return False
    
    def scroll_to_element(self, locator: Tuple[str, str]) -> None:
        """Scroll to element"""
        try:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)  # Allow scroll to complete
            self.logger.info(f"Scrolled to element: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to scroll to element: {locator}")
            raise
    
    def scroll_to_bottom(self) -> None:
        """Scroll to bottom of page"""
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.logger.info("Scrolled to bottom of page")
        except Exception as e:
            self.logger.error("Failed to scroll to bottom")
            raise
    
    def scroll_to_top(self) -> None:
        """Scroll to top of page"""
        try:
            self.driver.execute_script("window.scrollTo(0, 0);")
            self.logger.info("Scrolled to top of page")
        except Exception as e:
            self.logger.error("Failed to scroll to top")
            raise
    
    def hover_over_element(self, locator: Tuple[str, str]) -> None:
        """Hover over element"""
        try:
            element = self.find_element(locator)
            self.actions.move_to_element(element).perform()
            self.logger.info(f"Hovered over element: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to hover over element: {locator}")
            raise
    
    def drag_and_drop(self, source_locator: Tuple[str, str], target_locator: Tuple[str, str]) -> None:
        """Drag and drop element"""
        try:
            source = self.find_element(source_locator)
            target = self.find_element(target_locator)
            self.actions.drag_and_drop(source, target).perform()
            self.logger.info(f"Dragged element {source_locator} to {target_locator}")
        except Exception as e:
            self.logger.error(f"Failed to drag and drop element")
            raise
    
    def select_by_text(self, locator: Tuple[str, str], text: str) -> None:
        """Select option by text in dropdown"""
        try:
            from selenium.webdriver.support.ui import Select
            element = self.find_element(locator)
            select = Select(element)
            select.select_by_visible_text(text)
            self.logger.info(f"Selected '{text}' from dropdown: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to select option from dropdown: {locator}")
            raise
    
    def select_by_value(self, locator: Tuple[str, str], value: str) -> None:
        """Select option by value in dropdown"""
        try:
            from selenium.webdriver.support.ui import Select
            element = self.find_element(locator)
            select = Select(element)
            select.select_by_value(value)
            self.logger.info(f"Selected value '{value}' from dropdown: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to select value from dropdown: {locator}")
            raise
    
    def accept_alert(self) -> None:
        """Accept alert dialog"""
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
            self.logger.info("Accepted alert")
        except Exception as e:
            self.logger.error("Failed to accept alert")
            raise
    
    def dismiss_alert(self) -> None:
        """Dismiss alert dialog"""
        try:
            alert = self.driver.switch_to.alert
            alert.dismiss()
            self.logger.info("Dismissed alert")
        except Exception as e:
            self.logger.error("Failed to dismiss alert")
            raise
    
    def get_alert_text(self) -> str:
        """Get alert text"""
        try:
            alert = self.driver.switch_to.alert
            text = alert.text
            self.logger.info(f"Got alert text: {text}")
            return text
        except Exception as e:
            self.logger.error("Failed to get alert text")
            raise
    
    def switch_to_frame(self, frame_locator: Tuple[str, str]) -> None:
        """Switch to iframe"""
        try:
            frame = self.find_element(frame_locator)
            self.driver.switch_to.frame(frame)
            self.logger.info(f"Switched to frame: {frame_locator}")
        except Exception as e:
            self.logger.error(f"Failed to switch to frame: {frame_locator}")
            raise
    
    def switch_to_default_content(self) -> None:
        """Switch back to default content"""
        try:
            self.driver.switch_to.default_content()
            self.logger.info("Switched to default content")
        except Exception as e:
            self.logger.error("Failed to switch to default content")
            raise
    
    def wait_for_page_title(self, title: str, timeout: Optional[int] = None) -> None:
        """Wait for page title to match"""
        wait_time = timeout or config.get_timeout()
        wait = WebDriverWait(self.driver, wait_time)
        
        try:
            wait.until(EC.title_is(title))
            self.logger.info(f"Page title matched: {title}")
        except TimeoutException:
            self.logger.error(f"Page title did not match: {title}")
            raise
    
    def wait_for_url_contains(self, url_part: str, timeout: Optional[int] = None) -> None:
        """Wait for URL to contain specific part"""
        wait_time = timeout or config.get_timeout()
        wait = WebDriverWait(self.driver, wait_time)
        
        try:
            wait.until(EC.url_contains(url_part))
            self.logger.info(f"URL contains: {url_part}")
        except TimeoutException:
            self.logger.error(f"URL does not contain: {url_part}")
            raise
    
    def get_current_url(self) -> str:
        """Get current URL"""
        url = self.driver.current_url
        self.logger.info(f"Current URL: {url}")
        return url
    
    def get_page_title(self) -> str:
        """Get page title"""
        title = self.driver.title
        self.logger.info(f"Page title: {title}")
        return title
    
    def refresh_page(self) -> None:
        """Refresh current page"""
        try:
            self.driver.refresh()
            self._wait_for_page_load()
            self.logger.info("Page refreshed")
        except Exception as e:
            self.logger.error("Failed to refresh page")
            raise
    
    def go_back(self) -> None:
        """Go back to previous page"""
        try:
            self.driver.back()
            self._wait_for_page_load()
            self.logger.info("Went back to previous page")
        except Exception as e:
            self.logger.error("Failed to go back")
            raise
    
    def go_forward(self) -> None:
        """Go forward to next page"""
        try:
            self.driver.forward()
            self._wait_for_page_load()
            self.logger.info("Went forward to next page")
        except Exception as e:
            self.logger.error("Failed to go forward")
            raise
    
    def take_screenshot(self, name: str) -> str:
        """Take screenshot"""
        return self.screenshot_manager.take_screenshot(name)
    
    def start_performance_tracking(self) -> None:
        """Start performance tracking"""
        self.start_time = time.time()
        self.logger.info("Started performance tracking")
    
    def end_performance_tracking(self) -> float:
        """End performance tracking and return duration"""
        if self.start_time is None:
            raise ValueError("Performance tracking not started")
        
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        self.logger.info(f"Performance tracking ended. Duration: {duration:.2f} seconds")
        return duration
    
    def execute_js(self, script: str, *args) -> Any:
        """Execute JavaScript code"""
        try:
            result = self.driver.execute_script(script, *args)
            self.logger.info(f"Executed JavaScript: {script}")
            return result
        except Exception as e:
            self.logger.error(f"Failed to execute JavaScript: {script}")
            raise
    
    def wait_for_ajax(self, timeout: int = 10) -> None:
        """Wait for AJAX requests to complete"""
        try:
            self.wait.until(
                lambda driver: driver.execute_script("return jQuery.active == 0")
            )
            self.logger.info("AJAX requests completed")
        except TimeoutException:
            self.logger.warning("AJAX wait timeout")
        except Exception:
            # jQuery might not be available
            self.logger.debug("jQuery not available, skipping AJAX wait")
    
    def get_cookies(self) -> List[Dict[str, Any]]:
        """Get all cookies"""
        cookies = self.driver.get_cookies()
        self.logger.info(f"Retrieved {len(cookies)} cookies")
        return cookies
    
    def add_cookie(self, name: str, value: str, **kwargs) -> None:
        """Add cookie"""
        try:
            self.driver.add_cookie({
                'name': name,
                'value': value,
                **kwargs
            })
            self.logger.info(f"Added cookie: {name}")
        except Exception as e:
            self.logger.error(f"Failed to add cookie: {name}")
            raise
    
    def delete_cookie(self, name: str) -> None:
        """Delete cookie by name"""
        try:
            self.driver.delete_cookie(name)
            self.logger.info(f"Deleted cookie: {name}")
        except Exception as e:
            self.logger.error(f"Failed to delete cookie: {name}")
            raise
    
    def clear_cookies(self) -> None:
        """Clear all cookies"""
        try:
            self.driver.delete_all_cookies()
            self.logger.info("Cleared all cookies")
        except Exception as e:
            self.logger.error("Failed to clear cookies")
            raise 