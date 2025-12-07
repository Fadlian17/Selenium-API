import requests
import pytest

def test_get_user_detail_success():
    """Test positive: Mendapatkan detail user by email (email harus valid)"""
    url = "https://automationexercise.com/api/getUserDetailByEmail"
    params = {"email": "user@example.com"}
    response = requests.get(url, params=params)
    assert response.status_code == 200
    data = response.json()
    assert "user" in data

def test_get_user_detail_missing_param():
    """Test negative: Parameter email tidak diisi"""
    url = "https://automationexercise.com/api/getUserDetailByEmail"
    response = requests.get(url)
    assert response.status_code == 400
    assert "Bad request, email parameter is missing" in response.text
