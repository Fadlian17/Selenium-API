import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
from datetime import datetime

@pytest.fixture
def setup_browser():
    service = Service("drivers/chromedriver-linux64/chromedriver")  # path ke chromedriver
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.get("https://automationteststore.com/")
    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # hook result
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("setup_browser")
        if driver:
            screenshot_dir = "screenshots/failed"
            os.makedirs(screenshot_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{item.name}_{timestamp}.png"
            destination_file = os.path.join(screenshot_dir, file_name)
            driver.save_screenshot(destination_file)
            # Attach ke HTML report
            if "extra" in rep.longrepr:
                rep.longrepr["extra"].append(pytest_html.extras.image(destination_file))
            else:
                rep.extra = [pytest_html.extras.image(destination_file)]