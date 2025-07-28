import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any


class CustomHTMLReporter:
    """Custom HTML reporter for API test results"""
    
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        self.results = []
        self.start_time = None
        self.end_time = None
        
        # API list from automationexercise.com
        self.api_list = {
            "API 1": {
                "name": "Get All Products List",
                "url": "https://automationexercise.com/api/productsList",
                "method": "GET",
                "expected_code": 200,
                "description": "Get all products list"
            },
            "API 2": {
                "name": "POST To All Products List",
                "url": "https://automationexercise.com/api/productsList",
                "method": "POST",
                "expected_code": 405,
                "description": "Should return method not supported"
            },
            "API 3": {
                "name": "Get All Brands List",
                "url": "https://automationexercise.com/api/brandsList",
                "method": "GET",
                "expected_code": 200,
                "description": "Get all brands list"
            },
            "API 4": {
                "name": "PUT To All Brands List",
                "url": "https://automationexercise.com/api/brandsList",
                "method": "PUT",
                "expected_code": 405,
                "description": "Should return method not supported"
            },
            "API 5": {
                "name": "POST To Search Product",
                "url": "https://automationexercise.com/api/searchProduct",
                "method": "POST",
                "expected_code": 200,
                "description": "Search products with parameter"
            },
            "API 6": {
                "name": "POST To Search Product without parameter",
                "url": "https://automationexercise.com/api/searchProduct",
                "method": "POST",
                "expected_code": 400,
                "description": "Should return bad request"
            },
            "API 7": {
                "name": "POST To Verify Login with valid details",
                "url": "https://automationexercise.com/api/verifyLogin",
                "method": "POST",
                "expected_code": [200, 404],
                "description": "Verify login with valid credentials"
            },
            "API 8": {
                "name": "POST To Verify Login without email parameter",
                "url": "https://automationexercise.com/api/verifyLogin",
                "method": "POST",
                "expected_code": 400,
                "description": "Should return bad request"
            },
            "API 9": {
                "name": "DELETE To Verify Login",
                "url": "https://automationexercise.com/api/verifyLogin",
                "method": "DELETE",
                "expected_code": 405,
                "description": "Should return method not supported"
            },
            "API 10": {
                "name": "POST To Verify Login with invalid details",
                "url": "https://automationexercise.com/api/verifyLogin",
                "method": "POST",
                "expected_code": 404,
                "description": "Should return user not found"
            },
            "API 11": {
                "name": "POST To Create/Register User Account",
                "url": "https://automationexercise.com/api/createAccount",
                "method": "POST",
                "expected_code": 201,
                "description": "Create new user account"
            },
            "API 12": {
                "name": "DELETE METHOD To Delete User Account",
                "url": "https://automationexercise.com/api/deleteAccount",
                "method": "DELETE",
                "expected_code": 200,
                "description": "Delete user account"
            },
            "API 13": {
                "name": "PUT METHOD To Update User Account",
                "url": "https://automationexercise.com/api/updateAccount",
                "method": "PUT",
                "expected_code": 200,
                "description": "Update user account"
            },
            "API 14": {
                "name": "GET user account detail by email",
                "url": "https://automationexercise.com/api/getUserDetailByEmail",
                "method": "GET",
                "expected_code": 200,
                "description": "Get user details by email"
            }
        }
    
    def start_test_session(self):
        """Start test session"""
        self.start_time = datetime.now()
        self.results = []
    
    def add_test_result(self, api_id: str, test_name: str, status: str, 
                       actual_code: int = None, expected_code: Any = None,
                       response_time: float = None, error_message: str = None):
        """Add test result"""
        result = {
            "api_id": api_id,
            "test_name": test_name,
            "status": status,  # PASS, FAIL, SKIP
            "actual_code": actual_code,
            "expected_code": expected_code,
            "response_time": response_time,
            "error_message": error_message,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
    
    def end_test_session(self):
        """End test session"""
        self.end_time = datetime.now()
    
    def generate_html_report(self, filename: str = None):
        """Generate HTML report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"api_test_report_{timestamp}.html"
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Calculate statistics
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.results if r["status"] == "FAIL"])
        skipped_tests = len([r for r in self.results if r["status"] == "SKIP"])
        
        duration = (self.end_time - self.start_time).total_seconds() if self.end_time else 0
        
        # Generate HTML content
        html_content = self._generate_html_content(
            total_tests, passed_tests, failed_tests, skipped_tests, duration
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📊 HTML Report generated: {filepath}")
        return filepath
    
    def _generate_html_content(self, total: int, passed: int, failed: int, skipped: int, duration: float):
        """Generate HTML content"""
        success_rate = (passed / total * 100) if total > 0 else 0
        
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Test Report - AutomationExercise.com</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .stats-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.9em;
        }}
        
        .passed {{ color: #28a745; }}
        .failed {{ color: #dc3545; }}
        .skipped {{ color: #ffc107; }}
        .total {{ color: #007bff; }}
        
        .api-list {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .api-list h2 {{
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #dee2e6;
            margin: 0;
        }}
        
        .api-item {{
            border-bottom: 1px solid #dee2e6;
            padding: 20px;
            transition: background-color 0.3s;
        }}
        
        .api-item:hover {{
            background-color: #f8f9fa;
        }}
        
        .api-item:last-child {{
            border-bottom: none;
        }}
        
        .api-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        
        .api-title {{
            font-weight: bold;
            font-size: 1.1em;
        }}
        
        .api-status {{
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
        }}
        
        .status-pass {{
            background-color: #d4edda;
            color: #155724;
        }}
        
        .status-fail {{
            background-color: #f8d7da;
            color: #721c24;
        }}
        
        .status-skip {{
            background-color: #fff3cd;
            color: #856404;
        }}
        
        .api-details {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 10px;
        }}
        
        .detail-item {{
            font-size: 0.9em;
        }}
        
        .detail-label {{
            font-weight: bold;
            color: #666;
        }}
        
        .method-get {{ color: #28a745; }}
        .method-post {{ color: #007bff; }}
        .method-put {{ color: #ffc107; }}
        .method-delete {{ color: #dc3545; }}
        
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .api-details {{
                grid-template-columns: 1fr;
            }}
            
            .stats-container {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 API Test Report</h1>
            <p>AutomationExercise.com API Testing Results</p>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-number total">{total}</div>
                <div class="stat-label">Total Tests</div>
            </div>
            <div class="stat-card">
                <div class="stat-number passed">{passed}</div>
                <div class="stat-label">Passed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number failed">{failed}</div>
                <div class="stat-label">Failed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number skipped">{skipped}</div>
                <div class="stat-label">Skipped</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{success_rate:.1f}%</div>
                <div class="stat-label">Success Rate</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{duration:.2f}s</div>
                <div class="stat-label">Duration</div>
            </div>
        </div>
        
        <div class="api-list">
            <h2>📋 API Test Results</h2>
            {self._generate_api_results_html()}
        </div>
        
        <div class="footer">
            <p>Report generated by SeleniumHigh Framework</p>
            <p>Target: <a href="https://automationexercise.com/api_list" target="_blank">automationexercise.com/api_list</a></p>
        </div>
    </div>
</body>
</html>
        """
    
    def _generate_api_results_html(self):
        """Generate HTML for API results"""
        html = ""
        
        for api_id, api_info in self.api_list.items():
            # Find corresponding test result
            result = next((r for r in self.results if api_id in r["test_name"]), None)
            
            if result:
                status_class = f"status-{result['status'].lower()}"
                status_text = result['status']
            else:
                status_class = "status-skip"
                status_text = "NOT TESTED"
            
            method_class = f"method-{api_info['method'].lower()}"
            
            html += f"""
            <div class="api-item">
                <div class="api-header">
                    <div class="api-title">{api_id}: {api_info['name']}</div>
                    <div class="api-status {status_class}">{status_text}</div>
                </div>
                <div class="api-details">
                    <div class="detail-item">
                        <div class="detail-label">Method:</div>
                        <span class="{method_class}">{api_info['method']}</span>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">URL:</div>
                        <a href="{api_info['url']}" target="_blank">{api_info['url']}</a>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Expected Code:</div>
                        {api_info['expected_code']}
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Description:</div>
                        {api_info['description']}
                    </div>
                    {self._generate_result_details_html(result)}
                </div>
            </div>
            """
        
        return html
    
    def _generate_result_details_html(self, result):
        """Generate HTML for test result details"""
        if not result:
            return ""
        
        details = ""
        
        if result.get("actual_code"):
            details += f"""
            <div class="detail-item">
                <div class="detail-label">Actual Code:</div>
                {result['actual_code']}
            </div>
            """
        
        if result.get("response_time"):
            details += f"""
            <div class="detail-item">
                <div class="detail-label">Response Time:</div>
                {result['response_time']:.3f}s
            </div>
            """
        
        if result.get("error_message"):
            details += f"""
            <div class="detail-item" style="grid-column: 1 / -1;">
                <div class="detail-label">Error:</div>
                <div style="color: #dc3545; font-family: monospace; background: #f8f9fa; padding: 5px; border-radius: 3px;">
                    {result['error_message']}
                </div>
            </div>
            """
        
        return details 