import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from .base_reporter import BaseReporter


class HTMLReporter(BaseReporter):
    """HTML reporter for API test results"""
    
    def __init__(self, output_dir="reports", template_dir=None):
        super().__init__(output_dir)
        self.template_dir = template_dir or os.path.join(os.path.dirname(__file__), "templates")
        
        # API list from automationexercise.com
        self.api_list = self._load_api_definitions()
    
    def _load_api_definitions(self) -> Dict[str, Dict[str, Any]]:
        """Load API definitions from configuration"""
        return {
            "API 1": {
                "name": "Get All Products List",
                "url": "https://automationexercise.com/api/productsList",
                "method": "GET",
                "expected_code": 200,
                "description": "Get all products list",
                "category": "Product"
            },
            "API 2": {
                "name": "POST To All Products List",
                "url": "https://automationexercise.com/api/productsList",
                "method": "POST",
                "expected_code": 405,
                "description": "Should return method not supported",
                "category": "Product"
            },
            "API 3": {
                "name": "Get All Brands List",
                "url": "https://automationexercise.com/api/brandsList",
                "method": "GET",
                "expected_code": 200,
                "description": "Get all brands list",
                "category": "Brand"
            },
            "API 4": {
                "name": "PUT To All Brands List",
                "url": "https://automationexercise.com/api/brandsList",
                "method": "PUT",
                "expected_code": 405,
                "description": "Should return method not supported",
                "category": "Brand"
            },
            "API 5": {
                "name": "POST To Search Product",
                "url": "https://automationexercise.com/api/searchProduct",
                "method": "POST",
                "expected_code": 200,
                "description": "Search products with parameter",
                "category": "Product"
            },
            "API 6": {
                "name": "POST To Search Product without parameter",
                "url": "https://automationexercise.com/api/searchProduct",
                "method": "POST",
                "expected_code": 400,
                "description": "Should return bad request",
                "category": "Product"
            },
            "API 7": {
                "name": "POST To Verify Login with valid details",
                "url": "https://automationexercise.com/api/verifyLogin",
                "method": "POST",
                "expected_code": [200, 404],
                "description": "Verify login with valid credentials",
                "category": "Authentication"
            },
            "API 8": {
                "name": "POST To Verify Login without email parameter",
                "url": "https://automationexercise.com/api/verifyLogin",
                "method": "POST",
                "expected_code": 400,
                "description": "Should return bad request",
                "category": "Authentication"
            },
            "API 9": {
                "name": "DELETE To Verify Login",
                "url": "https://automationexercise.com/api/verifyLogin",
                "method": "DELETE",
                "expected_code": 405,
                "description": "Should return method not supported",
                "category": "Authentication"
            },
            "API 10": {
                "name": "POST To Verify Login with invalid details",
                "url": "https://automationexercise.com/api/verifyLogin",
                "method": "POST",
                "expected_code": 404,
                "description": "Should return user not found",
                "category": "Authentication"
            },
            "API 11": {
                "name": "POST To Create/Register User Account",
                "url": "https://automationexercise.com/api/createAccount",
                "method": "POST",
                "expected_code": 201,
                "description": "Create new user account",
                "category": "User Management"
            },
            "API 12": {
                "name": "DELETE METHOD To Delete User Account",
                "url": "https://automationexercise.com/api/deleteAccount",
                "method": "DELETE",
                "expected_code": 200,
                "description": "Delete user account",
                "category": "User Management"
            },
            "API 13": {
                "name": "PUT METHOD To Update User Account",
                "url": "https://automationexercise.com/api/updateAccount",
                "method": "PUT",
                "expected_code": 200,
                "description": "Update user account",
                "category": "User Management"
            },
            "API 14": {
                "name": "GET user account detail by email",
                "url": "https://automationexercise.com/api/getUserDetailByEmail",
                "method": "GET",
                "expected_code": 200,
                "description": "Get user details by email",
                "category": "User Management"
            }
        }
    
    def add_api_result(self, api_id: str, test_name: str, status: str, 
                      actual_code: int = None, expected_code: Any = None,
                      response_time: float = None, error_message: str = None,
                      response_data: Dict = None):
        """Add API test result with enhanced data"""
        result = {
            "api_id": api_id,
            "test_name": test_name,
            "status": status,
            "actual_code": actual_code,
            "expected_code": expected_code,
            "response_time": response_time,
            "error_message": error_message,
            "response_data": response_data,
            "category": self.api_list.get(api_id, {}).get("category", "Unknown")
        }
        
        self.add_result(**result)
    
    def generate_report(self, filename: str = None) -> str:
        """Generate HTML report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"api_test_report_{timestamp}.html"
        
        self._ensure_output_dir()
        filepath = os.path.join(self.output_dir, filename)
        
        # Get statistics
        stats = self.get_statistics()
        
        # Generate HTML content
        html_content = self._generate_html_content(stats)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📊 HTML Report generated: {filepath}")
        return filepath
    
    def _generate_html_content(self, stats: Dict[str, Any]) -> str:
        """Generate HTML content with improved structure"""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Test Report - AutomationExercise.com</title>
    <style>
        {self._get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        {self._generate_header_html()}
        {self._generate_stats_html(stats)}
        {self._generate_api_results_html()}
        {self._generate_footer_html()}
    </div>
    
    <script>
        {self._get_javascript()}
    </script>
</body>
</html>
        """
    
    def _get_css_styles(self) -> str:
        """Get CSS styles"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .stats-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9em;
        }
        
        .passed { color: #28a745; }
        .failed { color: #dc3545; }
        .skipped { color: #ffc107; }
        .total { color: #007bff; }
        
        .api-list {
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .api-list h2 {
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #dee2e6;
            margin: 0;
        }
        
        .category-filter {
            padding: 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }
        
        .filter-buttons {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .filter-btn {
            padding: 8px 16px;
            border: 1px solid #dee2e6;
            background: white;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .filter-btn.active {
            background: #007bff;
            color: white;
            border-color: #007bff;
        }
        
        .filter-btn:hover {
            background: #e9ecef;
        }
        
        .api-item {
            border-bottom: 1px solid #dee2e6;
            padding: 20px;
            transition: background-color 0.3s;
        }
        
        .api-item:hover {
            background-color: #f8f9fa;
        }
        
        .api-item:last-child {
            border-bottom: none;
        }
        
        .api-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .api-title {
            font-weight: bold;
            font-size: 1.1em;
        }
        
        .api-status {
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
        }
        
        .status-pass {
            background-color: #d4edda;
            color: #155724;
        }
        
        .status-fail {
            background-color: #f8d7da;
            color: #721c24;
        }
        
        .status-skip {
            background-color: #fff3cd;
            color: #856404;
        }
        
        .api-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 10px;
        }
        
        .detail-item {
            font-size: 0.9em;
        }
        
        .detail-label {
            font-weight: bold;
            color: #666;
        }
        
        .method-get { color: #28a745; }
        .method-post { color: #007bff; }
        .method-put { color: #ffc107; }
        .method-delete { color: #dc3545; }
        
        .footer {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
        }
        
        .hidden {
            display: none;
        }
        
        @media (max-width: 768px) {
            .api-details {
                grid-template-columns: 1fr;
            }
            
            .stats-container {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .filter-buttons {
                justify-content: center;
            }
        }
        """
    
    def _generate_header_html(self) -> str:
        """Generate header HTML"""
        return f"""
        <div class="header">
            <h1>🚀 API Test Report</h1>
            <p>AutomationExercise.com API Testing Results</p>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        """
    
    def _generate_stats_html(self, stats: Dict[str, Any]) -> str:
        """Generate statistics HTML"""
        return f"""
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-number total">{stats['total']}</div>
                <div class="stat-label">Total Tests</div>
            </div>
            <div class="stat-card">
                <div class="stat-number passed">{stats['passed']}</div>
                <div class="stat-label">Passed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number failed">{stats['failed']}</div>
                <div class="stat-label">Failed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number skipped">{stats['skipped']}</div>
                <div class="stat-label">Skipped</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['success_rate']:.1f}%</div>
                <div class="stat-label">Success Rate</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['duration']:.2f}s</div>
                <div class="stat-label">Duration</div>
            </div>
        </div>
        """
    
    def _generate_api_results_html(self) -> str:
        """Generate API results HTML with category filtering"""
        # Get unique categories
        categories = list(set(api.get("category", "Unknown") for api in self.api_list.values()))
        
        filter_html = f"""
        <div class="category-filter">
            <h3>Filter by Category:</h3>
            <div class="filter-buttons">
                <button class="filter-btn active" data-category="all">All Categories</button>
                {''.join(f'<button class="filter-btn" data-category="{cat}">{cat}</button>' for cat in categories)}
            </div>
        </div>
        """
        
        api_items_html = ""
        for api_id, api_info in self.api_list.items():
            # Find corresponding test result
            result = next((r for r in self.results if api_id in r.get("test_name", "")), None)
            
            if result:
                status_class = f"status-{result['status'].lower()}"
                status_text = result['status']
            else:
                status_class = "status-skip"
                status_text = "NOT TESTED"
            
            method_class = f"method-{api_info['method'].lower()}"
            category = api_info.get("category", "Unknown")
            
            api_items_html += f"""
            <div class="api-item" data-category="{category}">
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
        
        return f"""
        <div class="api-list">
            <h2>📋 API Test Results</h2>
            {filter_html}
            {api_items_html}
        </div>
        """
    
    def _generate_result_details_html(self, result: Optional[Dict[str, Any]]) -> str:
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
    
    def _generate_footer_html(self) -> str:
        """Generate footer HTML"""
        return """
        <div class="footer">
            <p>Report generated by SeleniumHigh Framework</p>
            <p>Target: <a href="https://automationexercise.com/api_list" target="_blank">automationexercise.com/api_list</a></p>
        </div>
        """
    
    def _get_javascript(self) -> str:
        """Get JavaScript for interactive features"""
        return """
        // Category filtering
        document.addEventListener('DOMContentLoaded', function() {
            const filterButtons = document.querySelectorAll('.filter-btn');
            const apiItems = document.querySelectorAll('.api-item');
            
            filterButtons.forEach(button => {
                button.addEventListener('click', function() {
                    const category = this.getAttribute('data-category');
                    
                    // Update active button
                    filterButtons.forEach(btn => btn.classList.remove('active'));
                    this.classList.add('active');
                    
                    // Filter API items
                    apiItems.forEach(item => {
                        if (category === 'all' || item.getAttribute('data-category') === category) {
                            item.classList.remove('hidden');
                        } else {
                            item.classList.add('hidden');
                        }
                    });
                });
            });
        });
        """ 