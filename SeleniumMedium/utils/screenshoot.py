import os

def save_screenshot(driver, filename="screenshots/screen.png"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    driver.save_screenshot(filename)
    print(f"📸 Screenshot saved to {filename}")
