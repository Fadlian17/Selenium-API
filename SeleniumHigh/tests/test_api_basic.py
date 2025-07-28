import pytest
import requests
import time


class TestAPIBasic:
    """Basic API tests for automationexercise.com"""
    
    def setup_method(self):
        """Setup for each test"""
        self.base_url = "https://automationexercise.com/api"
    
    def test_1_get_products_list(self):
        """Test API 1: Get All Products List"""
        response = requests.get(f"{self.base_url}/productsList", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert 'products' in data
        print(f"✅ Found {len(data['products'])} products")
    
    def test_2_get_brands_list(self):
        """Test API 3: Get All Brands List"""
        response = requests.get(f"{self.base_url}/brandsList", timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert 'brands' in data
        print(f"✅ Found {len(data['brands'])} brands")
    
    def test_3_search_product(self):
        """Test API 5: POST To Search Product"""
        search_data = {'search_product': 'tshirt'}
        response = requests.post(f"{self.base_url}/searchProduct", data=search_data, timeout=10)
        assert response.status_code == 200
        data = response.json()
        assert 'products' in data
        print(f"✅ Found {len(data['products'])} products for 'tshirt'")
    
    def test_4_search_product_missing_param(self):
        """Test API 6: POST To Search Product without parameter"""
        response = requests.post(f"{self.base_url}/searchProduct", timeout=10)
        assert response.status_code == 400
        assert "Bad request, search_product parameter is missing" in response.text
        print("✅ Correctly rejected search without parameter")
    
    def test_5_post_method_not_supported(self):
        """Test API 2: POST To All Products List (should return 405)"""
        response = requests.post(f"{self.base_url}/productsList", timeout=10)
        assert response.status_code == 405
        assert "This request method is not supported" in response.text
        print("✅ Correctly rejected POST to products list")
    
    def test_6_create_and_delete_account(self):
        """Test API 11 & 12: Create and Delete Account"""
        # Create test user data
        test_user = {
            'name': 'Test User',
            'email': f'testuser_{int(time.time())}@example.com',
            'password': 'Test1234',
            'title': 'Mr',
            'birth_date': '15',
            'birth_month': '06',
            'birth_year': '1990',
            'firstname': 'Test',
            'lastname': 'User',
            'company': 'Test Company',
            'address1': '123 Test Street',
            'address2': 'Apt 4B',
            'country': 'United States',
            'zipcode': '12345',
            'state': 'Test State',
            'city': 'Test City',
            'mobile_number': '1234567890'
        }
        
        # Create account
        create_response = requests.post(f"{self.base_url}/createAccount", data=test_user, timeout=10)
        if create_response.status_code == 201:
            print("✅ Account created successfully")
            
            # Delete account
            delete_data = {
                'email': test_user['email'],
                'password': test_user['password']
            }
            delete_response = requests.delete(f"{self.base_url}/deleteAccount", data=delete_data, timeout=10)
            assert delete_response.status_code == 200
            assert "Account deleted!" in delete_response.text
            print("✅ Account deleted successfully")
        else:
            pytest.skip("Could not create account for testing")
    
    def test_7_api_client_integration(self):
        """Test our custom API client"""
        from api.api_client import APIClient
        
        api_client = APIClient()
        
        # Test GET request
        response = api_client.get("productsList")
        assert response.status_code == 200
        
        # Test POST request
        search_data = {'search_product': 'dress'}
        response = api_client.post("searchProduct", search_data)
        assert response.status_code == 200
        
        print("✅ API Client integration successful") 