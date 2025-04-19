import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

@pytest.fixture
def setup_browser():
    service = Service("drivers/chromedriver-linux64/chromedriver")  # path ke chromedriver
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.get("https://automationteststore.com/")
    yield driver
    driver.quit()
