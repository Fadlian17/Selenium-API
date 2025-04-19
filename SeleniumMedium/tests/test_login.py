from pages.login_page import LoginPage

def test_success_login(setup_browser):
    driver = setup_browser
    login_page = LoginPage(driver)
    login_page.login("testuser", "password123")
    assert "My Account" in driver.title
