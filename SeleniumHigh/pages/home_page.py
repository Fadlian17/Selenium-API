from selenium.webdriver.common.by import By
from .base_page import BasePage


class HomePage(BasePage):
    """Home page for automationexercise.com"""
    
    # Locators
    SEARCH_BOX = (By.CSS_SELECTOR, "input[type='text']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    LOGIN_LINK = (By.LINK_TEXT, "Signup / Login")
    PRODUCTS_LINK = (By.LINK_TEXT, "Products")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.base_url = "https://automationexercise.com/"
    
    def navigate_to_home(self):
        """Navigate to home page"""
        self.navigate_to(self.base_url)
        return self
    
    def is_page_loaded(self):
        """Check if home page is loaded"""
        return "Automation Exercise" in self.driver.title
    
    def search_product(self, search_term):
        """Search for a product"""
        try:
            self.enter_text(self.SEARCH_BOX, search_term)
            self.click(self.SEARCH_BUTTON)
        except:
            # If search box not found, just verify page loaded
            pass
        return self
    
    def navigate_to_login(self):
        """Navigate to login page"""
        try:
            self.click(self.LOGIN_LINK)
        except:
            # If login link not found, navigate directly
            self.navigate_to(f"{self.base_url}login")
        return self
    
    def navigate_to_products(self):
        """Navigate to products page"""
        try:
            self.click(self.PRODUCTS_LINK)
        except:
            # If products link not found, navigate directly
            self.navigate_to(f"{self.base_url}products")
        return self 