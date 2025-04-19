from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    def go_to_cart(self):
        cart_link = (By.ID, "cart_checkout1")
        self.click(cart_link)
