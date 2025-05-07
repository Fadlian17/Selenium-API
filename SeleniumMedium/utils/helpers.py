from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def wait_for_element(driver, by, value, timeout=10):
    """Menunggu elemen sampai tampil di halaman."""
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))


def wait_and_click(driver, by, value, timeout=10):
    """Menunggu elemen dan melakukan klik."""
    element = wait_for_element(driver, by, value, timeout)
    element.click()


def wait_and_fill(driver, by, value, text, timeout=10):
    """Menunggu elemen input dan mengisi teks."""
    element = wait_for_element(driver, by, value, timeout)
    element.clear()
    element.send_keys(text)


def is_element_present(driver, by, value):
    """Memeriksa apakah elemen tersedia di halaman."""
    try:
        driver.find_element(by, value)
        return True
    except:
        return False
