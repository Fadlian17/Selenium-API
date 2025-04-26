from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json
import time
import os

# Setup options
options = Options()
options.add_argument("--auto-open-devtools-for-tabs")
options.add_argument("--headless=new")  # Headless mode yang kompatibel (new)
options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

# Start WebDriver
driver = webdriver.Chrome(options=options)
driver.set_window_size(1280, 800)
driver.get("https://automationteststore.com/")

# Wait for search bar to be visible
try:
    search_input = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.NAME, "search_query"))
    )
    print("🔍 Search input found!")
except:
    print("❌ Search input NOT found. Exiting...")
    driver.quit()
    exit(1)

# Type and press Enter
search_input.send_keys("skincare")
search_input.send_keys(Keys.RETURN)

# Wait for search result to appear
time.sleep(3)

# Screenshot
os.makedirs("screenshots", exist_ok=True)
screenshot_path = os.path.join("screenshots", "search_result.png")
driver.save_screenshot(screenshot_path)
print(f"📸 Screenshot saved at: {screenshot_path}")

# Extract network logs
logs = driver.get_log("performance")
api_calls = []

for entry in logs:
    log = json.loads(entry["message"])["message"]
    if (
        log["method"] == "Network.requestWillBeSent"
        and "request" in log["params"]
        and log["params"]["request"]["url"].startswith("https://")
    ):
        api_url = log["params"]["request"]["url"]
        method = log["params"]["request"].get("method", "GET")
        api_calls.append({"method": method, "url": api_url})

# Save API list
os.makedirs("api_logs", exist_ok=True)
with open("api_logs/api_calls.json", "w") as f:
    json.dump(api_calls, f, indent=2)

print("📋 API Calls Captured:")
for api in api_calls:
    print(f"{api['method']} - {api['url']}")

print("✅ Test finished. UI and API automation complete.")
driver.quit()
