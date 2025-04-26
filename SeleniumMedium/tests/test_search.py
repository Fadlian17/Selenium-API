from pages.home_page import HomePage
from utils.network_capture import capture_api_calls
from utils.screenshoot import save_screenshot
import time

def test_search_product(setup_browser):
    driver = setup_browser
    home_page = HomePage(driver)

    try:
        home_page.search_product("Skinsheen Bronzer Stick")
    except Exception as e:
        save_screenshot(driver, "screenshots/search_error.png")
        raise e

    time.sleep(3)  # Wait for search result page load

    # Save success screenshot
    save_screenshot(driver, "screenshots/search_result.png")

    # Capture API Calls
    capture_api_calls(driver, "api_logs/api_calls.json")

    # Validate product appears
    assert "Skinsheen Bronzer Stick" in driver.page_source