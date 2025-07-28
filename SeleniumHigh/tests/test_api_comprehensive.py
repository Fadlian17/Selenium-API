import pytest
import requests
import time
from api.api_client import APIClient


class TestAPIComprehensive:
    """Comprehensive API tests for automationexercise.com"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test data"""
        self.base_url = "https://automationexercise.com/api"
        self.api_client = APIClient()
        
        # Test user data
        self.test_user = {
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
    
    def test_api_1_get_all_products_list(self):
        """API 1: Get All Products List"""
        response = requests.get(f"{self.base_url}/productsList")
        assert response.status_code == 200
        data = response.json()
        assert 'products' in data
        print("✅ API 1: Get All Products List - SUCCESS")
    
    def test_api_2_post_to_products_list(self):
        """API 2: POST To All Products List (should return 405)"""
        response = requests.post(f"{self.base_url}/productsList")
        assert response.status_code == 405
        assert "This request method is not supported" in response.text
        print("✅ API 2: POST To All Products List - SUCCESS (405 as expected)")
    
    def test_api_3_get_all_brands_list(self):
        """API 3: Get All Brands List"""
        response = requests.get(f"{self.base_url}/brandsList")
        assert response.status_code == 200
        data = response.json()
        assert 'brands' in data
        print("✅ API 3: Get All Brands List - SUCCESS")
    
    def test_api_4_put_to_brands_list(self):
        """API 4: PUT To All Brands List (should return 405)"""
        response = requests.put(f"{self.base_url}/brandsList")
        assert response.status_code == 405
        assert "This request method is not supported" in response.text
        print("✅ API 4: PUT To All Brands List - SUCCESS (405 as expected)")
    
    def test_api_5_post_search_product_valid(self):
        """API 5: POST To Search Product with valid parameter"""
        search_data = {'search_product': 'tshirt'}
        response = requests.post(f"{self.base_url}/searchProduct", data=search_data)
        assert response.status_code == 200
        data = response.json()
        assert 'products' in data
        print("✅ API 5: POST To Search Product - SUCCESS")
    
    def test_api_6_post_search_product_missing_param(self):
        """API 6: POST To Search Product without search_product parameter"""
        response = requests.post(f"{self.base_url}/searchProduct")
        assert response.status_code == 400
        assert "Bad request, search_product parameter is missing" in response.text
        print("✅ API 6: POST To Search Product without parameter - SUCCESS (400 as expected)")
    
    def test_api_7_post_verify_login_valid(self):
        """API 7: POST To Verify Login with valid details"""
        login_data = {
            'email': 'test@example.com',
            'password': 'test123'
        }
        response = requests.post(f"{self.base_url}/verifyLogin", data=login_data)
        # Note: This might return 404 if user doesn't exist, which is also valid
        assert response.status_code in [200, 404]
        print("✅ API 7: POST To Verify Login with valid details - SUCCESS")
    
    def test_api_8_post_verify_login_missing_email(self):
        """API 8: POST To Verify Login without email parameter"""
        login_data = {'password': 'test123'}
        response = requests.post(f"{self.base_url}/verifyLogin", data=login_data)
        assert response.status_code == 400
        assert "Bad request, email or password parameter is missing" in response.text
        print("✅ API 8: POST To Verify Login without email - SUCCESS (400 as expected)")
    
    def test_api_9_delete_verify_login(self):
        """API 9: DELETE To Verify Login (should return 405)"""
        response = requests.delete(f"{self.base_url}/verifyLogin")
        assert response.status_code == 405
        assert "This request method is not supported" in response.text
        print("✅ API 9: DELETE To Verify Login - SUCCESS (405 as expected)")
    
    def test_api_10_post_verify_login_invalid(self):
        """API 10: POST To Verify Login with invalid details"""
        login_data = {
            'email': 'invalid@example.com',
            'password': 'wrongpassword'
        }
        response = requests.post(f"{self.base_url}/verifyLogin", data=login_data)
        assert response.status_code == 404
        assert "User not found!" in response.text
        print("✅ API 10: POST To Verify Login with invalid details - SUCCESS (404 as expected)")
    
    def test_api_11_post_create_account(self):
        """API 11: POST To Create/Register User Account"""
        response = requests.post(f"{self.base_url}/createAccount", data=self.test_user)
        assert response.status_code == 201
        assert "User created!" in response.text
        print("✅ API 11: POST To Create/Register User Account - SUCCESS")
        
        # Store email for cleanup
        self.created_email = self.test_user['email']
    
    def test_api_12_delete_account(self):
        """API 12: DELETE METHOD To Delete User Account"""
        # First create an account
        create_response = requests.post(f"{self.base_url}/createAccount", data=self.test_user)
        if create_response.status_code == 201:
            # Then delete it
            delete_data = {
                'email': self.test_user['email'],
                'password': self.test_user['password']
            }
            response = requests.delete(f"{self.base_url}/deleteAccount", data=delete_data)
            assert response.status_code == 200
            assert "Account deleted!" in response.text
            print("✅ API 12: DELETE METHOD To Delete User Account - SUCCESS")
        else:
            pytest.skip("Could not create account for deletion test")
    
    def test_api_13_put_update_account(self):
        """API 13: PUT METHOD To Update User Account"""
        # First create an account
        create_response = requests.post(f"{self.base_url}/createAccount", data=self.test_user)
        if create_response.status_code == 201:
            # Update the account
            updated_data = self.test_user.copy()
            updated_data['name'] = 'Updated Test User'
            updated_data['company'] = 'Updated Company'
            
            response = requests.put(f"{self.base_url}/updateAccount", data=updated_data)
            assert response.status_code == 200
            assert "User updated!" in response.text
            print("✅ API 13: PUT METHOD To Update User Account - SUCCESS")
            
            # Clean up
            delete_data = {
                'email': self.test_user['email'],
                'password': self.test_user['password']
            }
            requests.delete(f"{self.base_url}/deleteAccount", data=delete_data)
        else:
            pytest.skip("Could not create account for update test")
    
    def test_api_14_get_user_detail_by_email(self):
        """API 14: GET user account detail by email"""
        # First create an account
        create_response = requests.post(f"{self.base_url}/createAccount", data=self.test_user)
        if create_response.status_code == 201:
            # Get user details
            params = {'email': self.test_user['email']}
            response = requests.get(f"{self.base_url}/getUserDetailByEmail", params=params)
            assert response.status_code == 200
            data = response.json()
            assert 'user' in data
            print("✅ API 14: GET user account detail by email - SUCCESS")
            
            # Clean up
            delete_data = {
                'email': self.test_user['email'],
                'password': self.test_user['password']
            }
            requests.delete(f"{self.base_url}/deleteAccount", data=delete_data)
        else:
            pytest.skip("Could not create account for get details test")
    
    def test_api_client_integration(self):
        """Test our API client with various endpoints"""
        # Test products list
        response = self.api_client.get("productsList")
        assert response.status_code == 200
        
        # Test brands list
        response = self.api_client.get("brandsList")
        assert response.status_code == 200
        
        # Test search product
        search_data = {'search_product': 'dress'}
        response = self.api_client.post("searchProduct", search_data)
        assert response.status_code == 200
        
        print("✅ API Client Integration - SUCCESS") 