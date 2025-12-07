import requests
import pytest

def test_delete_account_success():
    """Test positive: Hapus user account (email & password harus valid)"""
    url = "https://automationexercise.com/api/deleteAccount"
    data = {"email": "user@example.com", "password": "Test1234"}
    response = requests.delete(url, data=data)
    assert response.status_code == 200
    assert "Account deleted!" in response.text

def test_delete_account_missing_param():
    """Test negative: Parameter tidak lengkap"""
    url = "https://automationexercise.com/api/deleteAccount"
    data = {"email": "user@example.com"}  # password missing
    response = requests.delete(url, data=data)
    assert response.status_code == 400
    assert "Bad request, email or password parameter is missing" in response.text
