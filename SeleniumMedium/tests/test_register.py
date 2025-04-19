import random
import string
import pytest
from selenium.webdriver.common.by import By

def random_string(length=6):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def test_register_user(setup_browser):
    driver = setup_browser
    driver.get("https://automationteststore.com/index.php?rt=account/create")

    # Generate random data
    firstname = "Fadlian"
    lastname = "QA"
    email = f"{random_string(8)}@mailinator.com"
    username = f"user_{random_string(5)}"
    password = "Password123"

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
    driver.find_element(By.ID, "AccountFrm_newsletter1").click()  # Subscribe newsletter
    driver.find_element(By.NAME, "agree").click()  # Agree terms

    # Submit form
    driver.find_element(By.XPATH, "//button[@title='Continue']").click()

    # Verifikasi sukses register
    success_title = driver.title
    assert "Your Account Has Been Created!" in success_title or "Account Created" in success_title
