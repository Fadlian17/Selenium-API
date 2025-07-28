#!/usr/bin/env python3
"""
API Test Runner with Custom HTML Reporter
Runs all API tests for automationexercise.com and generates HTML report
"""

import sys
import os
import time
import requests
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.html_reporter import CustomHTMLReporter


def test_api_1_get_products_list(reporter):
    """Test API 1: Get All Products List"""
    start_time = time.time()
    try:
        response = requests.get("https://automationexercise.com/api/productsList", timeout=10)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            if 'products' in data:
                reporter.add_test_result(
                    "API 1", "Get All Products List", "PASS",
                    response.status_code, 200, response_time
                )
                print(f"✅ API 1: Found {len(data['products'])} products")
                return True
            else:
                reporter.add_test_result(
                    "API 1", "Get All Products List", "FAIL",
                    response.status_code, 200, response_time,
                    "Response does not contain 'products' key"
                )
                print("❌ API 1: Response format incorrect")
                return False
        else:
            reporter.add_test_result(
                "API 1", "Get All Products List", "FAIL",
                response.status_code, 200, response_time,
                f"Expected 200, got {response.status_code}"
            )
            print(f"❌ API 1: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        response_time = time.time() - start_time
        reporter.add_test_result(
            "API 1", "Get All Products List", "FAIL",
            None, 200, response_time, str(e)
        )
        print(f"❌ API 1: Error - {e}")
        return False


def test_api_2_post_products_list(reporter):
    """Test API 2: POST To All Products List (should return 405)"""
    start_time = time.time()
    try:
        response = requests.post("https://automationexercise.com/api/productsList", timeout=10)
        response_time = time.time() - start_time
        
        if response.status_code == 405:
            reporter.add_test_result(
                "API 2", "POST To All Products List", "PASS",
                response.status_code, 405, response_time
            )
            print("✅ API 2: Correctly rejected POST (405)")
            return True
        else:
            reporter.add_test_result(
                "API 2", "POST To All Products List", "FAIL",
                response.status_code, 405, response_time,
                f"Expected 405, got {response.status_code}"
            )
            print(f"❌ API 2: Expected 405, got {response.status_code}")
            return False
    except Exception as e:
        response_time = time.time() - start_time
        reporter.add_test_result(
            "API 2", "POST To All Products List", "FAIL",
            None, 405, response_time, str(e)
        )
        print(f"❌ API 2: Error - {e}")
        return False


def test_api_3_get_brands_list(reporter):
    """Test API 3: Get All Brands List"""
    start_time = time.time()
    try:
        response = requests.get("https://automationexercise.com/api/brandsList", timeout=10)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            if 'brands' in data:
                reporter.add_test_result(
                    "API 3", "Get All Brands List", "PASS",
                    response.status_code, 200, response_time
                )
                print(f"✅ API 3: Found {len(data['brands'])} brands")
                return True
            else:
                reporter.add_test_result(
                    "API 3", "Get All Brands List", "FAIL",
                    response.status_code, 200, response_time,
                    "Response does not contain 'brands' key"
                )
                print("❌ API 3: Response format incorrect")
                return False
        else:
            reporter.add_test_result(
                "API 3", "Get All Brands List", "FAIL",
                response.status_code, 200, response_time,
                f"Expected 200, got {response.status_code}"
            )
            print(f"❌ API 3: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        response_time = time.time() - start_time
        reporter.add_test_result(
            "API 3", "Get All Brands List", "FAIL",
            None, 200, response_time, str(e)
        )
        print(f"❌ API 3: Error - {e}")
        return False


def test_api_5_search_product(reporter):
    """Test API 5: POST To Search Product"""
    start_time = time.time()
    try:
        search_data = {'search_product': 'tshirt'}
        response = requests.post("https://automationexercise.com/api/searchProduct", 
                               data=search_data, timeout=10)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            if 'products' in data:
                reporter.add_test_result(
                    "API 5", "POST To Search Product", "PASS",
                    response.status_code, 200, response_time
                )
                print(f"✅ API 5: Found {len(data['products'])} products for 'tshirt'")
                return True
            else:
                reporter.add_test_result(
                    "API 5", "POST To Search Product", "FAIL",
                    response.status_code, 200, response_time,
                    "Response does not contain 'products' key"
                )
                print("❌ API 5: Response format incorrect")
                return False
        else:
            reporter.add_test_result(
                "API 5", "POST To Search Product", "FAIL",
                response.status_code, 200, response_time,
                f"Expected 200, got {response.status_code}"
            )
            print(f"❌ API 5: Expected 200, got {response.status_code}")
            return False
    except Exception as e:
        response_time = time.time() - start_time
        reporter.add_test_result(
            "API 5", "POST To Search Product", "FAIL",
            None, 200, response_time, str(e)
        )
        print(f"❌ API 5: Error - {e}")
        return False


def test_api_6_search_product_missing_param(reporter):
    """Test API 6: POST To Search Product without parameter"""
    start_time = time.time()
    try:
        response = requests.post("https://automationexercise.com/api/searchProduct", timeout=10)
        response_time = time.time() - start_time
        
        if response.status_code == 400:
            reporter.add_test_result(
                "API 6", "POST To Search Product without parameter", "PASS",
                response.status_code, 400, response_time
            )
            print("✅ API 6: Correctly rejected search without parameter (400)")
            return True
        else:
            reporter.add_test_result(
                "API 6", "POST To Search Product without parameter", "FAIL",
                response.status_code, 400, response_time,
                f"Expected 400, got {response.status_code}"
            )
            print(f"❌ API 6: Expected 400, got {response.status_code}")
            return False
    except Exception as e:
        response_time = time.time() - start_time
        reporter.add_test_result(
            "API 6", "POST To Search Product without parameter", "FAIL",
            None, 400, response_time, str(e)
        )
        print(f"❌ API 6: Error - {e}")
        return False


def test_api_11_create_account(reporter):
    """Test API 11: POST To Create/Register User Account"""
    start_time = time.time()
    try:
        # Create unique test user
        timestamp = int(time.time())
        test_user = {
            'name': 'Test User',
            'email': f'testuser_{timestamp}@example.com',
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
        
        response = requests.post("https://automationexercise.com/api/createAccount", 
                               data=test_user, timeout=10)
        response_time = time.time() - start_time
        
        if response.status_code == 201:
            reporter.add_test_result(
                "API 11", "POST To Create/Register User Account", "PASS",
                response.status_code, 201, response_time
            )
            print("✅ API 11: Account created successfully")
            
            # Clean up - delete the account
            delete_data = {
                'email': test_user['email'],
                'password': test_user['password']
            }
            delete_response = requests.delete("https://automationexercise.com/api/deleteAccount", 
                                           data=delete_data, timeout=10)
            if delete_response.status_code == 200:
                print("✅ API 11: Account cleaned up successfully")
            
            return True
        else:
            reporter.add_test_result(
                "API 11", "POST To Create/Register User Account", "FAIL",
                response.status_code, 201, response_time,
                f"Expected 201, got {response.status_code}"
            )
            print(f"❌ API 11: Expected 201, got {response.status_code}")
            return False
    except Exception as e:
        response_time = time.time() - start_time
        reporter.add_test_result(
            "API 11", "POST To Create/Register User Account", "FAIL",
            None, 201, response_time, str(e)
        )
        print(f"❌ API 11: Error - {e}")
        return False


def run_all_api_tests():
    """Run all API tests and generate HTML report"""
    print("🚀 Starting API Tests for AutomationExercise.com")
    print("=" * 60)
    
    # Initialize reporter
    reporter = CustomHTMLReporter()
    reporter.start_test_session()
    
    # Run tests
    tests = [
        ("API 1", test_api_1_get_products_list),
        ("API 2", test_api_2_post_products_list),
        ("API 3", test_api_3_get_brands_list),
        ("API 5", test_api_5_search_product),
        ("API 6", test_api_6_search_product_missing_param),
        ("API 11", test_api_11_create_account),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func(reporter):
            passed += 1
        else:
            failed += 1
    
    # End session and generate report
    reporter.end_test_session()
    
    # Generate HTML report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = reporter.generate_html_report(f"api_test_report_{timestamp}.html")
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%" if (passed+failed) > 0 else "📈 Success Rate: 0%")
    print(f"📄 Report: {report_file}")
    print("=" * 60)
    
    return passed, failed


if __name__ == "__main__":
    try:
        passed, failed = run_all_api_tests()
        sys.exit(0 if failed == 0 else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Test execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1) 