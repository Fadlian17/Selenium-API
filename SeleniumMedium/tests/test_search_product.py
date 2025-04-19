from pages.home_page import HomePage

def test_search_product(setup_browser):
    driver = setup_browser
    home_page = HomePage(driver)
    home_page.search_product("Skinsheen Bronzer Stick")
    assert "Skinsheen Bronzer Stick" in driver.page_source
