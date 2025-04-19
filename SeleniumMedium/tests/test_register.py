import random
import string
import pytest
import os
from selenium.webdriver.common.by import By
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger("RegisterUserTest")

def random_string(length=6):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def capture_screenshot(driver, status="success"):
    folder = f"screenshots/{status}"
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(folder, f"register_{timestamp}.png")
    driver.save_screenshot(filepath)
    logger.info(f"Screenshot saved: {filepath}")

def test_register_user(setup_browser):
    driver = setup_browser
    try:
        driver.get("https://automationteststore.com/index.php?rt=account/create")
        logger.info("Opened registration page")

        # Generate random data
        firstname = "Fadlian"
        lastname = "QA"
        email = f"{random_string(8)}@mailinator.com"
        username = f"user_{random_string(5)}"
        password = "Password123"

        logger.info(f"Using username: {username}, email: {email}")

        # Isi form
        driver.find_element(By.ID, "AccountFrm_firstname").send_keys(firstname)
        driver.find_element(By.ID, "AccountFrm_lastname").send_keys(lastname)
        driver.find_element(By.ID, "AccountFrm_email").send_keys(email)
        driver.find_element(By.ID, "AccountFrm_telephone").send_keys("081234567890")
        driver.find_element(By.ID, "AccountFrm_fax").send_keys("021999999")
        driver.find_element(By.ID, "AccountFrm_company").send_keys("AutomationQA")
        driver.find_element(By.ID, "AccountFrm_address_1").send_keys("Jl. Testing Automation No.123")
        driver.find_element(By.ID, "AccountFrm_city").send_keys("Jakarta")
        driver.find_element(By.ID, "AccountFrm_postcode").send_keys("12345")

        # Country & Region
        country_select = driver.find_element(By.ID, "AccountFrm_country_id")
        country_select.find_element(By.XPATH, "//option[text()='United Kingdom']").click()

        region_select = driver.find_element(By.ID, "AccountFrm_zone_id")
        region_select.find_element(By.XPATH, "//option[contains(text(),'Aberdeen')]").click()

        # Login details
        driver.find_element(By.ID, "AccountFrm_loginname").send_keys(username)
        driver.find_element(By.ID, "AccountFrm_password").send_keys(password)
        driver.find_element(By.ID, "AccountFrm_confirm").send_keys(password)

        # Privacy policy + Newsletter
        driver.find_element(By.ID, "AccountFrm_newsletter1").click()
        driver.find_element(By.NAME, "agree").click()

        # Submit form
        driver.find_element(By.XPATH, "//button[@title='Continue']").click()

        # Verifikasi sukses register
        success_title = driver.title
        logger.info(f"Page title after register: {success_title}")

        assert "Your Account Has Been Created!" in success_title or "Account Created" in success_title

        logger.info(f"Register test passed for user: {username}")
        capture_screenshot(driver, "success")

    except Exception as e:
        logger.error(f"Register test failed: {str(e)}")
        capture_screenshot(driver, "failed")
        raise
