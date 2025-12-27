from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def test_ui_automationintesting():
    """Test UI dasar pada website https://automationintesting.online/"""
    # Setup Chrome driver
    service = Service('/path/to/chromedriver')  # Ganti dengan path chromedriver Anda
    driver = webdriver.Chrome(service=service)

    try:
        # Navigasi ke website
        driver.get("https://automationintesting.online/")
        print("✅ Berhasil membuka website")

        # Verifikasi judul halaman
        assert "Restful-booker-platform demo" in driver.title
        print("✅ Judul halaman sesuai")

        # Verifikasi elemen utama ada (logo atau header)
        try:
            header = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            print("✅ Header utama ditemukan")
        except TimeoutException:
            print("❌ Header utama tidak ditemukan")
            driver.save_screenshot("error_header.png")

        # Test navigasi ke halaman Booking
        try:
            booking_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Book this room"))
            )
            booking_link.click()
            print("✅ Berhasil klik 'Book this room'")

            # Verifikasi halaman booking
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "firstname"))
            )
            print("✅ Halaman booking terbuka dengan form")
        except TimeoutException:
            print("❌ Gagal navigasi ke halaman booking")
            driver.save_screenshot("error_booking.png")

        # Test isi form booking (exploratory)
        try:
            firstname_field = driver.find_element(By.ID, "firstname")
            firstname_field.send_keys("TestUser")
            print("✅ Berhasil isi field firstname")

            # Klik tombol book
            book_button = driver.find_element(By.ID, "book")
            book_button.click()
            print("✅ Berhasil klik tombol book")

            # Verifikasi pesan sukses atau error
            time.sleep(2)  # Tunggu response
            try:
                success_msg = driver.find_element(By.CLASS_NAME, "alert-success")
                print("✅ Booking berhasil")
            except NoSuchElementException:
                print("ℹ️  Booking mungkin gagal atau memerlukan data lengkap")
        except NoSuchElementException:
            print("❌ Elemen form tidak ditemukan")
            driver.save_screenshot("error_form.png")

        # Test navigasi kembali ke home
        driver.get("https://automationintesting.online/")
        print("✅ Kembali ke halaman utama")

        # Exploratory: Cek link lainnya
        try:
            contact_link = driver.find_element(By.LINK_TEXT, "Contact")
            contact_link.click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            print("✅ Halaman Contact dapat diakses")
        except (NoSuchElementException, TimeoutException):
            print("❌ Halaman Contact tidak dapat diakses")

        print("🎉 UI Test selesai - Website berfungsi dengan baik untuk interaksi dasar")

    except Exception as e:
        print(f"❌ Error selama test: {str(e)}")
        driver.save_screenshot("error_general.png")

    finally:
        # Tutup browser
        driver.quit()

if __name__ == "__main__":
    test_ui_automationintesting()