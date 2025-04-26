import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def setup_browser():
    options = Options()
    options.add_argument("--start-maximized")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    driver = webdriver.Chrome(options=options)
    driver.get("https://automationteststore.com/")
    yield driver
    driver.quit()
