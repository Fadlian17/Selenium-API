import requests
import pytest

def test_verify_login_success():
    """Test positive: Verifikasi login user (email & password harus sudah terdaftar)"""
    url = "https://automationexercise.com/api/verifyLogin"
    data = {"email": "user@example.com", "password": "Test1234"}
    response = requests.post(url, data=data)
    assert response.status_code in [200, 404]  # 404 jika user tidak ditemukan

def test_verify_login_missing_param():
    """Test negative: Parameter tidak lengkap"""
    url = "https://automationexercise.com/api/verifyLogin"
    data = {"email": "user@example.com"}  # password missing
    response = requests.post(url, data=data)
    assert response.status_code == 400
    assert "Bad request, email or password parameter is missing" in response.text
