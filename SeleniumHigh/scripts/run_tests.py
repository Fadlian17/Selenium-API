#!/usr/bin/env python3
"""
Test runner script for SeleniumHigh framework
Provides various options for running tests
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path
from typing import List, Optional


def run_command(command: List[str], description: str) -> bool:
    """Run a command and return success status"""
    print(f"🚀 {description}")
    print(f"Command: {' '.join(command)}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, check=True, capture_output=False)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False


def run_smoke_tests(browser: str = "chrome", headless: bool = True) -> bool:
    """Run smoke tests"""
    command = [
        "pytest", "tests/", "-m", "smoke", "-v",
        "--html=reports/smoke_report.html",
        "--self-contained-html"
    ]
    
    if headless:
        command.extend(["--headless"])
    
    env = os.environ.copy()
    env["SELENIUM_BROWSER"] = browser
    
    return run_command(command, f"Running smoke tests with {browser}")


def run_regression_tests(browser: str = "chrome", headless: bool = True) -> bool:
    """Run regression tests"""
    command = [
        "pytest", "tests/", "-m", "regression", "-v",
        "--html=reports/regression_report.html",
        "--self-contained-html"
    ]
    
    if headless:
        command.extend(["--headless"])
    
    env = os.environ.copy()
    env["SELENIUM_BROWSER"] = browser
    
    return run_command(command, f"Running regression tests with {browser}")


def run_e2e_tests(browser: str = "chrome", headless: bool = True) -> bool:
    """Run E2E tests"""
    command = [
        "pytest", "tests/", "-m", "e2e", "-v",
        "--html=reports/e2e_report.html",
        "--self-contained-html"
    ]
    
    if headless:
        command.extend(["--headless"])
    
    env = os.environ.copy()
    env["SELENIUM_BROWSER"] = browser
    
    return run_command(command, f"Running E2E tests with {browser}")


def run_api_tests() -> bool:
    """Run API tests"""
    command = [
        "pytest", "tests/", "-m", "api", "-v",
        "--html=reports/api_report.html",
        "--self-contained-html"
    ]
    
    return run_command(command, "Running API tests")


def run_visual_tests() -> bool:
    """Run visual regression tests"""
    command = [
        "pytest", "tests/", "-m", "visual", "-v",
        "--html=reports/visual_report.html",
        "--self-contained-html"
    ]
    
    return run_command(command, "Running visual regression tests")


def run_performance_tests() -> bool:
    """Run performance tests"""
    command = [
        "pytest", "tests/", "-m", "performance", "-v",
        "--html=reports/performance_report.html",
        "--self-contained-html"
    ]
    
    return run_command(command, "Running performance tests")


def run_mobile_tests() -> bool:
    """Run mobile tests"""
    command = [
        "pytest", "tests/", "-m", "mobile", "-v",
        "--html=reports/mobile_report.html",
        "--self-contained-html"
    ]
    
    return run_command(command, "Running mobile tests")


def run_all_tests(browser: str = "chrome", headless: bool = True, parallel: bool = False) -> bool:
    """Run all tests"""
    command = [
        "pytest", "tests/", "-v",
        "--html=reports/full_report.html",
        "--self-contained-html",
        "--json-report",
        "--json-report-file=reports/full_report.json"
    ]
    
    if headless:
        command.extend(["--headless"])
    
    if parallel:
        command.extend(["-n", "auto"])
    
    env = os.environ.copy()
    env["SELENIUM_BROWSER"] = browser
    
    return run_command(command, f"Running all tests with {browser}")


def run_specific_test(test_path: str, browser: str = "chrome", headless: bool = True) -> bool:
    """Run a specific test file or test method"""
    command = [
        "pytest", test_path, "-v",
        "--html=reports/specific_report.html",
        "--self-contained-html"
    ]
    
    if headless:
        command.extend(["--headless"])
    
    env = os.environ.copy()
    env["SELENIUM_BROWSER"] = browser
    
    return run_command(command, f"Running specific test: {test_path}")


def run_parallel_tests(browser: str = "chrome", workers: int = 4) -> bool:
    """Run tests in parallel"""
    command = [
        "pytest", "tests/", "-v", "-n", str(workers),
        "--html=reports/parallel_report.html",
        "--self-contained-html"
    ]
    
    env = os.environ.copy()
    env["SELENIUM_BROWSER"] = browser
    
    return run_command(command, f"Running tests in parallel with {workers} workers")


def run_with_coverage() -> bool:
    """Run tests with coverage report"""
    command = [
        "pytest", "tests/", "-v",
        "--cov=.",
        "--cov-report=html:reports/coverage",
        "--cov-report=term-missing",
        "--cov-fail-under=80"
    ]
    
    return run_command(command, "Running tests with coverage")


def run_failed_tests() -> bool:
    """Run only failed tests from last run"""
    command = [
        "pytest", "--lf", "-v",
        "--html=reports/failed_report.html",
        "--self-contained-html"
    ]
    
    return run_command(command, "Running failed tests")


def run_slow_tests() -> bool:
    """Run slow tests"""
    command = [
        "pytest", "tests/", "-m", "slow", "-v",
        "--html=reports/slow_report.html",
        "--self-contained-html"
    ]
    
    return run_command(command, "Running slow tests")


def run_security_tests() -> bool:
    """Run security tests"""
    command = [
        "pytest", "tests/", "-m", "security", "-v",
        "--html=reports/security_report.html",
        "--self-contained-html"
    ]
    
    return run_command(command, "Running security tests")


def run_accessibility_tests() -> bool:
    """Run accessibility tests"""
    command = [
        "pytest", "tests/", "-m", "accessibility", "-v",
        "--html=reports/accessibility_report.html",
        "--self-contained-html"
    ]
    
    return run_command(command, "Running accessibility tests")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="SeleniumHigh Test Runner")
    
    # Test type options
    parser.add_argument("--smoke", action="store_true", help="Run smoke tests")
    parser.add_argument("--regression", action="store_true", help="Run regression tests")
    parser.add_argument("--e2e", action="store_true", help="Run E2E tests")
    parser.add_argument("--api", action="store_true", help="Run API tests")
    parser.add_argument("--visual", action="store_true", help="Run visual regression tests")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    parser.add_argument("--mobile", action="store_true", help="Run mobile tests")
    parser.add_argument("--security", action="store_true", help="Run security tests")
    parser.add_argument("--accessibility", action="store_true", help="Run accessibility tests")
    parser.add_argument("--slow", action="store_true", help="Run slow tests")
    parser.add_argument("--failed", action="store_true", help="Run failed tests from last run")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    
    # Browser options
    parser.add_argument("--browser", choices=["chrome", "firefox", "edge", "safari"], 
                       default="chrome", help="Browser to use for tests")
    parser.add_argument("--headless", action="store_true", default=True, 
                       help="Run browser in headless mode")
    parser.add_argument("--no-headless", action="store_true", 
                       help="Run browser in non-headless mode")
    
    # Execution options
    parser.add_argument("--parallel", action="store_true", help="Run tests in parallel")
    parser.add_argument("--workers", type=int, default=4, help="Number of parallel workers")
    parser.add_argument("--coverage", action="store_true", help="Run tests with coverage")
    
    # Specific test options
    parser.add_argument("--test", type=str, help="Run specific test file or test method")
    
    args = parser.parse_args()
    
    # Handle headless option
    headless = args.headless and not args.no_headless
    
    print("🚀 SeleniumHigh Test Runner")
    print("=" * 50)
    
    success = True
    
    # Run tests based on arguments
    if args.smoke:
        success &= run_smoke_tests(args.browser, headless)
    
    if args.regression:
        success &= run_regression_tests(args.browser, headless)
    
    if args.e2e:
        success &= run_e2e_tests(args.browser, headless)
    
    if args.api:
        success &= run_api_tests()
    
    if args.visual:
        success &= run_visual_tests()
    
    if args.performance:
        success &= run_performance_tests()
    
    if args.mobile:
        success &= run_mobile_tests()
    
    if args.security:
        success &= run_security_tests()
    
    if args.accessibility:
        success &= run_accessibility_tests()
    
    if args.slow:
        success &= run_slow_tests()
    
    if args.failed:
        success &= run_failed_tests()
    
    if args.coverage:
        success &= run_with_coverage()
    
    if args.test:
        success &= run_specific_test(args.test, args.browser, headless)
    
    if args.parallel:
        success &= run_parallel_tests(args.browser, args.workers)
    
    if args.all:
        success &= run_all_tests(args.browser, headless, args.parallel)
    
    # If no specific test type is selected, run all tests
    if not any([args.smoke, args.regression, args.e2e, args.api, args.visual, 
                args.performance, args.mobile, args.security, args.accessibility, 
                args.slow, args.failed, args.all, args.test, args.parallel]):
        success &= run_all_tests(args.browser, headless, args.parallel)
    
    print("=" * 50)
    if success:
        print("✅ All tests completed successfully!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main() 