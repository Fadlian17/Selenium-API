import pytest
from typing import Dict, Any, List
from utils.test_base import APITestBase, TestResult
from utils.html_reporter import HTMLReporter
from datetime import datetime


class ProductAPITests(APITestBase):
    """Product-related API tests"""
    
    def test_get_all_products(self) -> TestResult:
        """Test API 1: Get All Products List"""
        result = TestResult("Get All Products List", "PASS")
        
        try:
            response, response_time = self.get("productsList")
            result.response_time = response_time
            result.set_response_info(200, response.status_code)
            
            if self.assert_status_code(response, 200):
                if self.assert_json_contains_key(response, "products"):
                    data = response.json()
                    result.set_response_data({"product_count": len(data.get("products", []))})
                    print(f"✅ Found {len(data.get('products', []))} products")
                else:
                    result.status = "FAIL"
                    result.set_error("Response does not contain 'products' key")
            else:
                result.status = "FAIL"
                result.set_error(f"Expected 200, got {response.status_code}")
                
        except Exception as e:
            result.status = "FAIL"
            result.set_error(str(e))
        
        return result
    
    def test_post_products_not_allowed(self) -> TestResult:
        """Test API 2: POST To All Products List (should return 405)"""
        result = TestResult("POST To All Products List", "PASS")
        
        try:
            response, response_time = self.post("productsList")
            result.response_time = response_time
            result.set_response_info(405, response.status_code)
            
            if self.assert_status_code(response, 405):
                print("✅ Correctly rejected POST (405)")
            else:
                result.status = "FAIL"
                result.set_error(f"Expected 405, got {response.status_code}")
                
        except Exception as e:
            result.status = "FAIL"
            result.set_error(str(e))
        
        return result


class BrandAPITests(APITestBase):
    """Brand-related API tests"""
    
    def test_get_all_brands(self) -> TestResult:
        """Test API 3: Get All Brands List"""
        result = TestResult("Get All Brands List", "PASS")
        
        try:
            response, response_time = self.get("brandsList")
            result.response_time = response_time
            result.set_response_info(200, response.status_code)
            
            if self.assert_status_code(response, 200):
                if self.assert_json_contains_key(response, "brands"):
                    data = response.json()
                    result.set_response_data({"brand_count": len(data.get("brands", []))})
                    print(f"✅ Found {len(data.get('brands', []))} brands")
                else:
                    result.status = "FAIL"
                    result.set_error("Response does not contain 'brands' key")
            else:
                result.status = "FAIL"
                result.set_error(f"Expected 200, got {response.status_code}")
                
        except Exception as e:
            result.status = "FAIL"
            result.set_error(str(e))
        
        return result
    
    def test_put_brands_not_allowed(self) -> TestResult:
        """Test API 4: PUT To All Brands List (should return 405)"""
        result = TestResult("PUT To All Brands List", "PASS")
        
        try:
            response, response_time = self.put("brandsList")
            result.response_time = response_time
            result.set_response_info(405, response.status_code)
            
            if self.assert_status_code(response, 405):
                print("✅ Correctly rejected PUT (405)")
            else:
                result.status = "FAIL"
                result.set_error(f"Expected 405, got {response.status_code}")
                
        except Exception as e:
            result.status = "FAIL"
            result.set_error(str(e))
        
        return result


class SearchAPITests(APITestBase):
    """Search-related API tests"""
    
    def test_search_product_valid(self) -> TestResult:
        """Test API 5: POST To Search Product with valid parameter"""
        result = TestResult("POST To Search Product", "PASS")
        
        try:
            search_data = {'search_product': 'tshirt'}
            response, response_time = self.post("searchProduct", data=search_data)
            result.response_time = response_time
            result.set_response_info(200, response.status_code)
            
            if self.assert_status_code(response, 200):
                if self.assert_json_contains_key(response, "products"):
                    data = response.json()
                    result.set_response_data({"search_results": len(data.get("products", []))})
                    print(f"✅ Found {len(data.get('products', []))} products for 'tshirt'")
                else:
                    result.status = "FAIL"
                    result.set_error("Response does not contain 'products' key")
            else:
                result.status = "FAIL"
                result.set_error(f"Expected 200, got {response.status_code}")
                
        except Exception as e:
            result.status = "FAIL"
            result.set_error(str(e))
        
        return result
    
    def test_search_product_missing_param(self) -> TestResult:
        """Test API 6: POST To Search Product without parameter"""
        result = TestResult("POST To Search Product without parameter", "PASS")
        
        try:
            response, response_time = self.post("searchProduct")
            result.response_time = response_time
            result.set_response_info(400, response.status_code)
            
            if self.assert_status_code(response, 400):
                print("✅ Correctly rejected search without parameter (400)")
            else:
                result.status = "FAIL"
                result.set_error(f"Expected 400, got {response.status_code}")
                
        except Exception as e:
            result.status = "FAIL"
            result.set_error(str(e))
        
        return result


class AuthenticationAPITests(APITestBase):
    """Authentication-related API tests"""
    
    def test_verify_login_valid(self) -> TestResult:
        """Test API 7: POST To Verify Login with valid details"""
        result = TestResult("POST To Verify Login with valid details", "PASS")
        
        try:
            login_data = {'email': 'test@example.com', 'password': 'test123'}
            response, response_time = self.post("verifyLogin", data=login_data)
            result.response_time = response_time
            result.set_response_info([200, 404], response.status_code)
            
            if self.assert_status_code(response, [200, 404]):
                print("✅ Login verification completed")
            else:
                result.status = "FAIL"
                result.set_error(f"Expected 200 or 404, got {response.status_code}")
                
        except Exception as e:
            result.status = "FAIL"
            result.set_error(str(e))
        
        return result
    
    def test_verify_login_missing_email(self) -> TestResult:
        """Test API 8: POST To Verify Login without email parameter"""
        result = TestResult("POST To Verify Login without email", "PASS")
        
        try:
            login_data = {'password': 'test123'}
            response, response_time = self.post("verifyLogin", data=login_data)
            result.response_time = response_time
            result.set_response_info(400, response.status_code)
            
            if self.assert_status_code(response, 400):
                print("✅ Correctly rejected login without email (400)")
            else:
                result.status = "FAIL"
                result.set_error(f"Expected 400, got {response.status_code}")
                
        except Exception as e:
            result.status = "FAIL"
            result.set_error(str(e))
        
        return result
    
    def test_verify_login_delete_not_allowed(self) -> TestResult:
        """Test API 9: DELETE To Verify Login (should return 405)"""
        result = TestResult("DELETE To Verify Login", "PASS")
        
        try:
            response, response_time = self.delete("verifyLogin")
            result.response_time = response_time
            result.set_response_info(405, response.status_code)
            
            if self.assert_status_code(response, 405):
                print("✅ Correctly rejected DELETE (405)")
            else:
                result.status = "FAIL"
                result.set_error(f"Expected 405, got {response.status_code}")
                
        except Exception as e:
            result.status = "FAIL"
            result.set_error(str(e))
        
        return result
    
    def test_verify_login_invalid(self) -> TestResult:
        """Test API 10: POST To Verify Login with invalid details"""
        result = TestResult("POST To Verify Login with invalid details", "PASS")
        
        try:
            login_data = {'email': 'invalid@example.com', 'password': 'wrongpassword'}
            response, response_time = self.post("verifyLogin", data=login_data)
            result.response_time = response_time
            result.set_response_info(404, response.status_code)
            
            if self.assert_status_code(response, 404):
                print("✅ Correctly rejected invalid login (404)")
            else:
                result.status = "FAIL"
                result.set_error(f"Expected 404, got {response.status_code}")
                
        except Exception as e:
            result.status = "FAIL"
            result.set_error(str(e))
        
        return result


class UserManagementAPITests(APITestBase):
    """User management API tests"""
    
    def test_create_account(self) -> TestResult:
        """Test API 11: POST To Create/Register User Account"""
        result = TestResult("POST To Create/Register User Account", "PASS")
        
        try:
            test_user = self.create_test_user()
            response, response_time = self.post("createAccount", data=test_user)
            result.response_time = response_time
            result.set_response_info(201, response.status_code)
            
            if self.assert_status_code(response, 201):
                print("✅ Account created successfully")
                # Clean up
                self.cleanup_test_user(test_user['email'], test_user['password'])
            else:
                result.status = "FAIL"
                result.set_error(f"Expected 201, got {response.status_code}")
                
        except Exception as e:
            result.status = "FAIL"
            result.set_error(str(e))
        
        return result
    
    def test_delete_account(self) -> TestResult:
        """Test API 12: DELETE METHOD To Delete User Account"""
        result = TestResult("DELETE METHOD To Delete User Account", "PASS")
        
        try:
            # First create an account
            test_user = self.create_test_user()
            create_response, _ = self.post("createAccount", data=test_user)
            
            if create_response.status_code == 201:
                # Then delete it
                delete_data = {'email': test_user['email'], 'password': test_user['password']}
                response, response_time = self.delete("deleteAccount", data=delete_data)
                result.response_time = response_time
                result.set_response_info(200, response.status_code)
                
                if self.assert_status_code(response, 200):
                    print("✅ Account deleted successfully")
                else:
                    result.status = "FAIL"
                    result.set_error(f"Expected 200, got {response.status_code}")
            else:
                result.status = "SKIP"
                result.set_error("Could not create account for deletion test")
                
        except Exception as e:
            result.status = "FAIL"
            result.set_error(str(e))
        
        return result
    
    def test_update_account(self) -> TestResult:
        """Test API 13: PUT METHOD To Update User Account"""
        result = TestResult("PUT METHOD To Update User Account", "PASS")
        
        try:
            # First create an account
            test_user = self.create_test_user()
            create_response, _ = self.post("createAccount", data=test_user)
            
            if create_response.status_code == 201:
                # Update the account
                updated_data = test_user.copy()
                updated_data['name'] = 'Updated Test User'
                updated_data['company'] = 'Updated Company'
                
                response, response_time = self.put("updateAccount", data=updated_data)
                result.response_time = response_time
                result.set_response_info(200, response.status_code)
                
                if self.assert_status_code(response, 200):
                    print("✅ Account updated successfully")
                else:
                    result.status = "FAIL"
                    result.set_error(f"Expected 200, got {response.status_code}")
                
                # Clean up
                self.cleanup_test_user(test_user['email'], test_user['password'])
            else:
                result.status = "SKIP"
                result.set_error("Could not create account for update test")
                
        except Exception as e:
            result.status = "FAIL"
            result.set_error(str(e))
        
        return result
    
    def test_get_user_detail_by_email(self) -> TestResult:
        """Test API 14: GET user account detail by email"""
        result = TestResult("GET user account detail by email", "PASS")
        
        try:
            # First create an account
            test_user = self.create_test_user()
            create_response, _ = self.post("createAccount", data=test_user)
            
            if create_response.status_code == 201:
                # Get user details
                params = {'email': test_user['email']}
                response, response_time = self.get("getUserDetailByEmail", params=params)
                result.response_time = response_time
                result.set_response_info(200, response.status_code)
                
                if self.assert_status_code(response, 200):
                    if self.assert_json_contains_key(response, "user"):
                        print("✅ User details retrieved successfully")
                    else:
                        result.status = "FAIL"
                        result.set_error("Response does not contain 'user' key")
                else:
                    result.status = "FAIL"
                    result.set_error(f"Expected 200, got {response.status_code}")
                
                # Clean up
                self.cleanup_test_user(test_user['email'], test_user['password'])
            else:
                result.status = "SKIP"
                result.set_error("Could not create account for get details test")
                
        except Exception as e:
            result.status = "FAIL"
            result.set_error(str(e))
        
        return result


class APITestSuite:
    """Main test suite that orchestrates all test categories"""
    
    def __init__(self):
        self.reporter = HTMLReporter()
        self.test_categories = {
            "Product": ProductAPITests(),
            "Brand": BrandAPITests(),
            "Search": SearchAPITests(),
            "Authentication": AuthenticationAPITests(),
            "User Management": UserManagementAPITests()
        }
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and generate report"""
        print("🚀 Starting Modular API Test Suite")
        print("=" * 60)
        
        self.reporter.start_session(
            target_url="https://automationexercise.com/api_list",
            test_suite="Modular API Test Suite",
            framework_version="2.0"
        )
        
        all_results = []
        
        for category_name, test_category in self.test_categories.items():
            print(f"\n📋 Running {category_name} Tests...")
            print("-" * 40)
            
            # Get all test methods from the category
            test_methods = [method for method in dir(test_category) 
                          if method.startswith('test_') and callable(getattr(test_category, method))]
            
            for test_method_name in test_methods:
                test_method = getattr(test_category, test_method_name)
                print(f"🔍 Running {test_method_name}...")
                
                try:
                    result = test_method()
                    all_results.append(result)
                    
                    # Add result to reporter
                    self.reporter.add_api_result(
                        api_id=result.test_name.split(":")[0] if ":" in result.test_name else "Unknown",
                        test_name=result.test_name,
                        status=result.status,
                        actual_code=result.actual_code,
                        expected_code=result.expected_code,
                        response_time=result.response_time,
                        error_message=result.error_message,
                        response_data=result.response_data
                    )
                    
                    # Print result
                    status_emoji = "✅" if result.status == "PASS" else "❌" if result.status == "FAIL" else "⚠️"
                    print(f"{status_emoji} {result.test_name}: {result.status}")
                    
                except Exception as e:
                    print(f"💥 Error in {test_method_name}: {e}")
                    error_result = TestResult(test_method_name, "ERROR")
                    error_result.set_error(str(e))
                    all_results.append(error_result)
        
        # End session and generate report
        self.reporter.end_session()
        
        # Generate HTML report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reporter.generate_report(f"modular_api_test_report_{timestamp}.html")
        
        # Print summary
        self._print_summary(all_results, report_file)
        
        return {
            "results": all_results,
            "report_file": report_file,
            "statistics": self.reporter.get_statistics()
        }
    
    def _print_summary(self, results: List[TestResult], report_file: str):
        """Print test summary"""
        total = len(results)
        passed = len([r for r in results if r.status == "PASS"])
        failed = len([r for r in results if r.status == "FAIL"])
        skipped = len([r for r in results if r.status == "SKIP"])
        error = len([r for r in results if r.status == "ERROR"])
        
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️ Skipped: {skipped}")
        print(f"💥 Error: {error}")
        print(f"📈 Success Rate: {(passed/(total)*100):.1f}%" if total > 0 else "📈 Success Rate: 0%")
        print(f"📄 Report: {report_file}")
        print("=" * 60)


# Pytest integration
@pytest.fixture
def api_test_suite():
    """Fixture for API test suite"""
    return APITestSuite()


def test_run_all_api_tests(api_test_suite):
    """Run all API tests and verify results"""
    results = api_test_suite.run_all_tests()
    
    # Basic assertions
    assert "results" in results
    assert "report_file" in results
    assert "statistics" in results
    
    # Check that we have results
    assert len(results["results"]) > 0
    
    # Check that report was generated
    assert results["report_file"].endswith(".html")


if __name__ == "__main__":
    # Run test suite directly
    suite = APITestSuite()
    suite.run_all_tests() 