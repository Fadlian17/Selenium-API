from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def enter_text(self, locator, text):
        try:
            element = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(locator)
            )
            element.clear()
            element.send_keys(text)
        except TimeoutException:
            self.driver.save_screenshot("screenshots/ERROR_enter_text.png")
            raise Exception(f"❌ Failed to find and interact with element {locator}")

    def click(self, locator):
        try:
            element = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
        except TimeoutException:
            self.driver.save_screenshot("screenshots/ERROR_click.png")
            raise Exception(f"❌ Failed to find and click element {locator}")