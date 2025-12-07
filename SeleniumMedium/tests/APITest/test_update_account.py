import requests
import pytest

def test_update_account_success():
    """Test positive: Update user account (email & password harus valid)"""
    url = "https://automationexercise.com/api/updateAccount"
    data = {
        "email": "user@example.com",
        "password": "Test1234",
        "name": "UpdatedName"
    }
    response = requests.put(url, data=data)
    assert response.status_code == 200
    assert "Account updated!" in response.text

def test_update_account_missing_param():
    """Test negative: Parameter tidak lengkap"""
    url = "https://automationexercise.com/api/updateAccount"
    data = {
        "email": "user@example.com"
        # password missing
    }
    response = requests.put(url, data=data)
    assert response.status_code == 400
    assert "Bad request, email or password parameter is missing" in response.text
