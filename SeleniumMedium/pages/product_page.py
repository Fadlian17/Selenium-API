from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductPage(BasePage):
    def select_product_by_name(self, product_name):
        product_locator = (By.LINK_TEXT, product_name)
        self.click(product_locator)

    def add_to_cart(self):
        add_to_cart_button = (By.XPATH, "//a[@title='Add to Cart']")
        self.click(add_to_cart_button)
