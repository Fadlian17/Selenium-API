#!/usr/bin/env python3
"""
Modular API Test Runner with Custom HTML Reporter
Runs all API tests for automationexercise.com and generates HTML report
"""

import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.test_suite_modular import APITestSuite


def main():
    """Main function to run the test suite"""
    print("🚀 Starting Modular API Test Suite for AutomationExercise.com")
    print("=" * 70)
    
    try:
        # Create and run test suite
        suite = APITestSuite()
        results = suite.run_all_tests()
        
        # Exit with appropriate code
        if results["statistics"]["failed"] > 0:
            print(f"\n⚠️ Tests completed with {results['statistics']['failed']} failures")
            sys.exit(1)
        else:
            print(f"\n🎉 All tests passed successfully!")
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n⚠️ Test execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 