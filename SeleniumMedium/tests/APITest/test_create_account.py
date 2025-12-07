import requests
import pytest
import time

def test_create_account_success():
    """Test positive: Register user baru dengan data valid"""
    url = "https://automationexercise.com/api/createAccount"
    data = {
        "name": "TestUser",
        "email": f"testuser_{int(time.time())}@example.com",
        "password": "Test1234",
        "title": "Mr",
        "birth_date": "01",
        "birth_month": "01",
        "birth_year": "1990",
        "firstname": "Test",
        "lastname": "User",
        "company": "TestCompany",
        "address1": "Jl. Automation",
        "address2": "Suite 1",
        "country": "Indonesia",
        "zipcode": "12345",
        "state": "Jawa Barat",
        "city": "Bandung",
        "mobile_number": "08123456789"
    }
    response = requests.post(url, data=data)
    assert response.status_code == 201
    assert "User created!" in response.text

def test_create_account_missing_field():
    """Test negative: Register user baru dengan data tidak lengkap"""
    url = "https://automationexercise.com/api/createAccount"
    data = {
        "name": "TestUser",
        # email field missing intentionally
        "password": "Test1234"
    }
    response = requests.post(url, data=data)
    assert response.status_code == 400
    assert "Bad request" in response.text
