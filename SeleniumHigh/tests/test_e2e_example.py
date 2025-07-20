import pytest
import time
from typing import Dict, Any
from selenium.webdriver.common.by import By

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from api.api_client import APIClient


class TestE2EUserJourney:
    """End-to-End test scenarios for complete user journeys"""
    
    @pytest.mark.e2e
    @pytest.mark.smoke
    def test_complete_user_registration_and_login(self, setup_browser, api_client, test_user_data):
        """Test complete user registration and login flow"""
        driver = setup_browser
        home_page = HomePage(driver)
        login_page = LoginPage(driver)
        
        # Start performance tracking
        home_page.start_performance_tracking()
        
        try:
            # Step 1: Navigate to home page
            home_page.navigate_to_home()
            assert home_page.is_page_loaded()
            
            # Step 2: Navigate to registration
            home_page.navigate_to_register()
            assert login_page.is_register_page_loaded()
            
            # Step 3: Register new user
            user_data = test_user_data.copy()
            user_data['email'] = f"test_{int(time.time())}@example.com"
            
            login_page.register_user(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                password=user_data['password']
            )
            
            # Step 4: Verify registration success
            assert home_page.is_user_logged_in()
            assert home_page.get_welcome_message().contains(user_data['first_name'])
            
            # Step 5: Logout
            home_page.logout()
            assert not home_page.is_user_logged_in()
            
            # Step 6: Login with new account
            home_page.navigate_to_login()
            login_page.login(user_data['email'], user_data['password'])
            assert home_page.is_user_logged_in()
            
            # Performance assertion
            duration = home_page.end_performance_tracking()
            assert duration < 30, f"User journey took too long: {duration:.2f}s"
            
        except Exception as e:
            # Take screenshot on failure
            home_page.take_screenshot("e2e_registration_failed")
            raise
    
    @pytest.mark.e2e
    @pytest.mark.regression
    def test_complete_shopping_journey(self, setup_browser, api_client, test_user_data):
        """Test complete shopping journey from product search to checkout"""
        driver = setup_browser
        home_page = HomePage(driver)
        login_page = LoginPage(driver)
        product_page = ProductPage(driver)
        cart_page = CartPage(driver)
        
        # Start performance tracking
        home_page.start_performance_tracking()
        
        try:
            # Step 1: Login user
            home_page.navigate_to_login()
            login_page.login(test_user_data['email'], test_user_data['password'])
            assert home_page.is_user_logged_in()
            
            # Step 2: Search for product
            search_term = "laptop"
            home_page.search_product(search_term)
            assert home_page.is_search_results_displayed()
            
            # Step 3: Select first product
            home_page.click_first_product()
            assert product_page.is_product_page_loaded()
            
            # Step 4: Add product to cart
            product_name = product_page.get_product_name()
            product_price = product_page.get_product_price()
            product_page.add_to_cart()
            assert product_page.is_added_to_cart_message_displayed()
            
            # Step 5: View cart
            product_page.navigate_to_cart()
            assert cart_page.is_cart_page_loaded()
            assert cart_page.is_product_in_cart(product_name)
            assert cart_page.get_cart_total() == product_price
            
            # Step 6: Proceed to checkout
            cart_page.proceed_to_checkout()
            assert cart_page.is_checkout_page_loaded()
            
            # Performance assertion
            duration = home_page.end_performance_tracking()
            assert duration < 45, f"Shopping journey took too long: {duration:.2f}s"
            
        except Exception as e:
            # Take screenshot on failure
            home_page.take_screenshot("e2e_shopping_failed")
            raise
    
    @pytest.mark.e2e
    @pytest.mark.integration
    def test_api_ui_integration(self, setup_browser, api_client, test_user_data):
        """Test integration between API and UI"""
        driver = setup_browser
        home_page = HomePage(driver)
        login_page = LoginPage(driver)
        
        try:
            # Step 1: Create user via API
            user_data = test_user_data.copy()
            user_data['email'] = f"api_test_{int(time.time())}@example.com"
            
            api_response = api_client.post('/api/users', json_data=user_data)
            api_client.assert_status_code(api_response, 201)
            
            user_id = api_response.json()['id']
            
            # Step 2: Verify user exists via API
            get_response = api_client.get(f'/api/users/{user_id}')
            api_client.assert_status_code(get_response, 200)
            
            # Step 3: Login via UI with API-created user
            home_page.navigate_to_login()
            login_page.login(user_data['email'], user_data['password'])
            assert home_page.is_user_logged_in()
            
            # Step 4: Verify user data in UI matches API
            user_profile = home_page.get_user_profile()
            assert user_profile['email'] == user_data['email']
            assert user_profile['first_name'] == user_data['first_name']
            
            # Step 5: Update user via API
            updated_data = {'first_name': 'UpdatedName'}
            update_response = api_client.put(f'/api/users/{user_id}', json_data=updated_data)
            api_client.assert_status_code(update_response, 200)
            
            # Step 6: Verify update reflected in UI
            home_page.refresh_page()
            updated_profile = home_page.get_user_profile()
            assert updated_profile['first_name'] == 'UpdatedName'
            
        except Exception as e:
            home_page.take_screenshot("api_ui_integration_failed")
            raise
    
    @pytest.mark.e2e
    @pytest.mark.performance
    def test_performance_under_load(self, setup_browser, api_client):
        """Test application performance under simulated load"""
        driver = setup_browser
        home_page = HomePage(driver)
        
        # Performance metrics
        page_load_times = []
        api_response_times = []
        
        try:
            # Test multiple page loads
            for i in range(5):
                start_time = time.time()
                home_page.navigate_to_home()
                home_page.wait_for_page_load()
                load_time = time.time() - start_time
                page_load_times.append(load_time)
                
                # Test API calls
                api_start = time.time()
                api_response = api_client.get('/api/products')
                api_client.assert_status_code(api_response, 200)
                api_time = time.time() - api_start
                api_response_times.append(api_time)
            
            # Performance assertions
            avg_page_load = sum(page_load_times) / len(page_load_times)
            avg_api_response = sum(api_response_times) / len(api_response_times)
            
            assert avg_page_load < 3.0, f"Average page load time too high: {avg_page_load:.2f}s"
            assert avg_api_response < 1.0, f"Average API response time too high: {avg_api_response:.2f}s"
            assert max(page_load_times) < 5.0, f"Maximum page load time too high: {max(page_load_times):.2f}s"
            
        except Exception as e:
            home_page.take_screenshot("performance_test_failed")
            raise
    
    @pytest.mark.e2e
    @pytest.mark.visual
    def test_visual_regression(self, setup_browser, visual_testing_manager):
        """Test visual regression across different pages"""
        driver = setup_browser
        home_page = HomePage(driver)
        screenshot_manager = visual_testing_manager['screenshot_manager']
        
        try:
            # Take screenshots of key pages
            home_page.navigate_to_home()
            home_screenshot = screenshot_manager.take_screenshot("home_page")
            
            home_page.navigate_to_login()
            login_screenshot = screenshot_manager.take_screenshot("login_page")
            
            # Compare with baselines if they exist
            baseline_home = "screenshots/baseline/home_page.png"
            baseline_login = "screenshots/baseline/login_page.png"
            
            if os.path.exists(baseline_home):
                comparison = screenshot_manager.compare_screenshots(
                    baseline_home, home_screenshot, tolerance=0.95
                )
                assert comparison['similar'], f"Home page visual regression detected: {comparison['hash_similarity']:.3f}"
            
            if os.path.exists(baseline_login):
                comparison = screenshot_manager.compare_screenshots(
                    baseline_login, login_screenshot, tolerance=0.95
                )
                assert comparison['similar'], f"Login page visual regression detected: {comparison['hash_similarity']:.3f}"
            
        except Exception as e:
            screenshot_manager.take_screenshot("visual_regression_failed")
            raise
    
    @pytest.mark.e2e
    @pytest.mark.mobile
    def test_mobile_responsive_design(self, setup_browser_mobile):
        """Test mobile responsive design and functionality"""
        driver = setup_browser_mobile
        home_page = HomePage(driver)
        
        try:
            # Test mobile navigation
            home_page.navigate_to_home()
            assert home_page.is_page_loaded()
            
            # Test mobile menu
            home_page.open_mobile_menu()
            assert home_page.is_mobile_menu_displayed()
            
            # Test mobile search
            home_page.search_product("mobile")
            assert home_page.is_search_results_displayed()
            
            # Test mobile product view
            home_page.click_first_product()
            assert home_page.is_product_page_loaded()
            
            # Test mobile cart
            home_page.add_to_cart()
            assert home_page.is_added_to_cart_message_displayed()
            
        except Exception as e:
            home_page.take_screenshot("mobile_test_failed")
            raise
    
    @pytest.mark.e2e
    @pytest.mark.slow
    def test_complete_workflow_with_data_validation(self, setup_browser, api_client, database_connection):
        """Test complete workflow with database validation"""
        driver = setup_browser
        home_page = HomePage(driver)
        login_page = LoginPage(driver)
        
        try:
            # Create test data
            test_order = {
                'customer': {
                    'name': 'Test Customer',
                    'email': f'test_{int(time.time())}@example.com',
                    'phone': '1234567890'
                },
                'products': [
                    {'name': 'Test Product 1', 'quantity': 2, 'price': 29.99},
                    {'name': 'Test Product 2', 'quantity': 1, 'price': 49.99}
                ]
            }
            
            # Step 1: Create order via API
            api_response = api_client.post('/api/orders', json_data=test_order)
            api_client.assert_status_code(api_response, 201)
            order_id = api_response.json()['id']
            
            # Step 2: Verify order in database
            if database_connection:
                db_order = database_connection.execute(
                    "SELECT * FROM orders WHERE id = ?", (order_id,)
                ).fetchone()
                assert db_order is not None
                assert db_order['customer_email'] == test_order['customer']['email']
            
            # Step 3: View order in UI
            home_page.navigate_to_order(order_id)
            assert home_page.is_order_page_loaded()
            
            # Step 4: Verify order details in UI
            order_details = home_page.get_order_details()
            assert order_details['customer_name'] == test_order['customer']['name']
            assert order_details['total_amount'] == sum(p['price'] * p['quantity'] for p in test_order['products'])
            
            # Step 5: Update order status via API
            status_update = {'status': 'shipped'}
            update_response = api_client.put(f'/api/orders/{order_id}/status', json_data=status_update)
            api_client.assert_status_code(update_response, 200)
            
            # Step 6: Verify status update in UI
            home_page.refresh_page()
            updated_status = home_page.get_order_status()
            assert updated_status == 'shipped'
            
        except Exception as e:
            home_page.take_screenshot("workflow_validation_failed")
            raise


class TestE2ESecurity:
    """Security-focused E2E tests"""
    
    @pytest.mark.e2e
    @pytest.mark.security
    def test_xss_protection(self, setup_browser):
        """Test XSS protection in forms"""
        driver = setup_browser
        login_page = LoginPage(driver)
        
        try:
            # Test XSS payload in search
            xss_payload = "<script>alert('XSS')</script>"
            login_page.navigate_to_search()
            login_page.search_product(xss_payload)
            
            # Verify XSS payload is not executed
            alert_present = False
            try:
                alert = driver.switch_to.alert
                alert_present = True
                alert.dismiss()
            except:
                pass
            
            assert not alert_present, "XSS payload was executed"
            
        except Exception as e:
            login_page.take_screenshot("xss_test_failed")
            raise
    
    @pytest.mark.e2e
    @pytest.mark.security
    def test_sql_injection_protection(self, setup_browser, api_client):
        """Test SQL injection protection"""
        driver = setup_browser
        
        try:
            # Test SQL injection payload
            sql_payload = "'; DROP TABLE users; --"
            
            # Test in search
            api_response = api_client.get(f'/api/products?search={sql_payload}')
            api_client.assert_status_code(api_response, [200, 400, 404])
            
            # Verify no database error in response
            response_text = api_response.text.lower()
            assert 'sql' not in response_text
            assert 'database' not in response_text
            assert 'error' not in response_text
            
        except Exception as e:
            driver.save_screenshot("sql_injection_test_failed.png")
            raise


class TestE2EAccessibility:
    """Accessibility-focused E2E tests"""
    
    @pytest.mark.e2e
    @pytest.mark.accessibility
    def test_keyboard_navigation(self, setup_browser):
        """Test keyboard navigation accessibility"""
        driver = setup_browser
        home_page = HomePage(driver)
        
        try:
            home_page.navigate_to_home()
            
            # Test tab navigation
            home_page.press_tab()
            assert home_page.is_focus_on_element(home_page.SEARCH_BOX)
            
            home_page.press_tab()
            assert home_page.is_focus_on_element(home_page.SEARCH_BUTTON)
            
            # Test enter key
            home_page.press_enter()
            assert home_page.is_search_results_displayed()
            
        except Exception as e:
            home_page.take_screenshot("keyboard_navigation_failed")
            raise
    
    @pytest.mark.e2e
    @pytest.mark.accessibility
    def test_screen_reader_compatibility(self, setup_browser):
        """Test screen reader compatibility"""
        driver = setup_browser
        home_page = HomePage(driver)
        
        try:
            home_page.navigate_to_home()
            
            # Check for alt text on images
            images = driver.find_elements(By.TAG_NAME, "img")
            for img in images:
                alt_text = img.get_attribute("alt")
                assert alt_text is not None, "Image missing alt text"
                assert alt_text.strip() != "", "Image has empty alt text"
            
            # Check for ARIA labels
            elements_with_aria = driver.find_elements(By.CSS_SELECTOR, "[aria-label]")
            for element in elements_with_aria:
                aria_label = element.get_attribute("aria-label")
                assert aria_label is not None, "Element missing aria-label"
                assert aria_label.strip() != "", "Element has empty aria-label"
            
        except Exception as e:
            home_page.take_screenshot("accessibility_test_failed")
            raise 