from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    SEARCH_INPUT = (By.ID, "filter_keyword")  # ✅ Gunakan ID biar lebih cepat & akurat
    SEARCH_BUTTON = (By.CSS_SELECTOR, "div.button-in-search")  # ✅ Ganti ke div.button-in-search

    def search_product(self, product_name):
        print("🔍 Trying to search product...")
        self.enter_text(self.SEARCH_INPUT, product_name)
        self.click(self.SEARCH_BUTTON)

    def is_product_displayed(self, product_name):
        return product_name in self.driver.page_source