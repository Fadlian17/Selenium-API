from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage

def test_add_product_to_cart(setup_browser):
    driver = setup_browser
    home_page = HomePage(driver)
    product_page = ProductPage(driver)
    cart_page = CartPage(driver)

    home_page.search_product("Skinsheen Bronzer Stick")
    product_page.select_product_by_name("Skinsheen Bronzer Stick")
    product_page.add_to_cart()

    cart_page.go_to_cart()
    assert "Skinsheen Bronzer Stick" in driver.page_source
